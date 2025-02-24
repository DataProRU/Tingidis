import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# SMTP настройки
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")