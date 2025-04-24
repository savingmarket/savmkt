from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import telegram
import asyncio

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники (для продакшена укажите конкретные, например ["https://your-site.com"])
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],  # Разрешённые методы
    allow_headers=["Content-Type"],  # Разрешённые заголовки
)

# Конфигурация Telegram-бота
TELEGRAM_BOT_TOKEN = "7911856352:AAEm1xmOKLcUgV_Q8H6W5b9LUssWNewafKw"
CHAT_ID_1 = "-1002514693384"
CHAT_ID_2 = "-4759508105"

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

# Модель для валидации входных данных
class CallbackData(BaseModel):
    name: str
    phone: str
    ip: str
    country: str
    flag: str
    deviceType: str

# Модель для compare-формы
class CompareData(BaseModel):
    currency: str
    depositAmount: str
    investmentTerm: str
    investmentReadiness: str
    name: str
    email: str
    phone: str
    termsAccepted: bool
    ip: str
    country: str
    flag: str
    deviceType: str

# Обработчик для OPTIONS-запросов
@app.options("/submit")
async def options_submit():
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        }
    )

# Эндпоинт для получения данных (POST)
@app.post("/submit")
async def submit_callback(data: CallbackData):
    # Формируем сообщение
    message = (
        "New callback request\n\n"
        f"Name: {data.name}\n"
        f"Phone number: {data.phone}\n"
        f"IP: {data.ip}\n"
        f"Country: {data.country} {data.flag}\n"
        f"Device: {data.deviceType}"
    )

    # Отправляем сообщение в оба чата
    try:
        await bot.send_message(chat_id=CHAT_ID_1, text=message)
        await bot.send_message(chat_id=CHAT_ID_2, text=message)
        return {"status": "success"}
    except Exception as e:
        print(f"Ошибка отправки сообщения: {e}")
        return {"status": "error", "message": str(e)}

# Обработчик OPTIONS для /compare-submit
@app.options("/compare-submit")
async def options_compare_submit():
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        }
    )

# Эндпоинт для compare-формы
@app.post("/compare-submit")
async def submit_compare(data: CompareData):
    message = (
        "New rate request\n\n"
        f"Currency: {data.currency}\n"
        f"Deposit amount: {data.depositAmount}\n"
        f"Investment Term: {data.investmentTerm}\n"
        f"Investment Readiness: {data.investmentReadiness}\n"
        f"Name: {data.name}\n"
        f"Email: {data.email}\n"
        f"Phone number: {data.phone}\n"
        f"Agree with terms: {'Yes' if data.termsAccepted else 'No'}\n"
        f"IP: {data.ip}\n"
        f"Country: {data.country} {data.flag}\n"
        f"Device: {data.deviceType}"
    )
    try:
        await bot.send_message(chat_id=CHAT_ID_1, text=message)
        await bot.send_message(chat_id=CHAT_ID_2, text=message)
        return {"status": "success"}
    except Exception as e:
        print(f"Ошибка отправки сообщения: {e}")
        return {"status": "error", "message": str(e)}

# Запуск сервера с HTTPS
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        ssl_keyfile="/etc/ssl/private/selfsigned.key",
        ssl_certfile="/etc/ssl/certs/selfsigned.crt"
    )
