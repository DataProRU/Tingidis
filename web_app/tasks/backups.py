import io
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from celery import Celery
from config import SMTP_USER, SMTP_PASSWORD
from sqlalchemy.ext.asyncio import AsyncSession
from web_app.utils.reports import generate_excel_report

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery("tasks", broker="redis://localhost:6379/0")

@celery.task
def send_email_backup(email: str, db: AsyncSession = Depends(get_db)):
    excel_file = generate_excel_report(db)
    
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)

        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = email
        msg['Subject'] = "Backup Excel Report"

        # Прикрепляем файл Excel
        part = MIMEBase("application", "octet-stream")
        part.set_payload(excel_file.getvalue())
        
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename=report.xlsx",
        )
        msg.attach(part)

        # Отправляем письмо
        server.send_message(msg)

    # Очищаем BytesIO объект
    excel_file.close()