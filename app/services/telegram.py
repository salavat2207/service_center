import httpx
from ..config import settings


async def send_notification(chat_id: str, message: str):
	"""
	Отправляет уведомление в Telegram
	"""
	if not settings.TELEGRAM_BOT_TOKEN:
		print("Telegram Bot Token не настроен")
		return False

	url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
	payload = {
		"chat_id": chat_id,
		"text": message,
		"parse_mode": "HTML"
	}

	try:
		async with httpx.AsyncClient() as client:
			response = await client.post(url, json=payload)
			return response.status_code == 200
	except Exception as e:
		print(f"Ошибка отправки сообщения в телеграммы:: {e}")
		return False