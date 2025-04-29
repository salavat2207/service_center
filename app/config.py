# import os
# from pydantic_settings import BaseSettings
# from typing import Optional
#
#
# class Settings(BaseSettings):
# 	# База данных
# 	DATABASE_URL: str = "sqlite:///./service_center.db"
# 	# DATABASE_URL: str = "postgresql://user:password@localhost/service_center"
#
# 	# JWT
# 	SECRET_KEY: str = "YOUR_SECRET_KEY_HERE"  # В продакшене используйте безопасный ключ
# 	ALGORITHM: str = "HS256"
# 	ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
#
# 	# Email
# 	SMTP_SERVER: str = "smtp.gmail.com"
# 	SMTP_PORT: int = 587
# 	SMTP_USER: str = "your_email@gmail.com"
# 	SMTP_PASSWORD: str = "your_app_password"
#
# 	# Telegram
# 	TELEGRAM_BOT_TOKEN: Optional[str] = None
#
# 	class Config:
# 		env_file = ".env"
#
#
# settings = Settings()


from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # База данных
    DATABASE_URL: str = "sqlite:///./service_center.db"
    # DATABASE_URL: str = "postgresql://user:password@localhost/service_center"

    # JWT
    SECRET_KEY: str = "YOUR_SECRET_KEY_HERE"  # В продакшене используйте безопасный ключ
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Email
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "your_email@gmail.com"
    SMTP_PASSWORD: str = "your_app_password"

    # Telegram
    TELEGRAM_CHAT_ID: Optional[str] = None
    TELEGRAM_BOT_TOKEN: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"  # желательно указывать явно


settings = Settings()