import smtplib
from email.message import EmailMessage
import logger

from celery import Celery
from config import SMTP_USER, SMTP_PASSWORD

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery("tasks", broker="redis://localhost:6379/0")
# logger =


@celery.task
def send_email_backup(email: str):
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)

        msg = EmailMessage()
        msg.set_content(f"Backup has been completed.")
        msg["Subject"] = f"Backup"
        msg["From"] = SMTP_USER
        msg["To"] = email

        server.send_message(msg)