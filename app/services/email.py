import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ..config import settings


async def send_notification(recipient: str, subject: str, body: str):
	"""
	Отправляет уведомление по электронной почте
	"""
	message = MIMEMultipart()
	message["From"] = settings.SMTP_USER
	message["To"] = recipient
	message["Subject"] = subject

	message.attach(MIMEText(body, "plain"))

	try:
		await aiosmtplib.send(
			message,
			hostname=settings.SMTP_SERVER,
			port=settings.SMTP_PORT,
			username=settings.SMTP_USER,
			password=settings.SMTP_PASSWORD,
			use_tls=True
		)
		return True
	except Exception as e:
		print(f"Ошибка отправки письма: {e}")
		return False