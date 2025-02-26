import io
from fastapi import Depends
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from celery import Celery
from config import SMTP_USER, SMTP_PASSWORD, SMTP_HOST, SMTP_PORT
from sqlalchemy import select
from datetime import datetime, timedelta
from web_app.utils.reports import generate_excel_report
from web_app.database import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from web_app.models.backups import Backups
from web_app.database import get_db
import logging

celery = Celery("backups", broker="redis://localhost:6379/0")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@celery.task
def send_reserve_copies():
    db = SessionLocal()
    async_db: AsyncSession = Depends(get_db),
    try:
        excel_file = generate_excel_report(async_db)
        today = datetime.now().date()

        # Find all reserve copies that need to be sent today
        stmt = select(Backups).where(Backups.send_date == today)
        result = db.execute(stmt)
        reserve_copies = result.scalars().all()
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            for reserve_copy in reserve_copies:
                logger.info(f"Sending email to {reserve_copy.email}")
                logger.info(f"Attempting to connect to server")
                try:
                    server.login(SMTP_USER, SMTP_PASSWORD)

                    msg = MIMEMultipart()
                    msg['From'] = SMTP_USER
                    msg['To'] = reserve_copy.email
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

                    # Update send_date based on frequency
                    if reserve_copy.frequency == 1:
                        new_send_date = today + timedelta(days=7)
                    elif reserve_copy.frequency == 2:
                        new_send_date = today + timedelta(days=30)
                    elif reserve_copy.frequency == 3:
                        new_send_date = today + timedelta(days=90)
                    elif reserve_copy.frequency == 4:
                        new_send_date = today + timedelta(days=180)
                    elif reserve_copy.frequency == 5:
                        new_send_date = today + timedelta(days=365)

                    reserve_copy.send_date = new_send_date

                    db.commit()
                except Exception as e:
                    logger.error(f"Failed to send email to {reserve_copy.email}: {str(e)}")
                    db.rollback()

    finally:
        db.close()

    # Очищаем BytesIO объект
    excel_file.close()