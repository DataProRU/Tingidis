import io
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from celery import Celery
from config import SMTP_USER, SMTP_PASSWORD
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
from fastapi import Depends
from web_app.utils.reports import generate_excel_report
from web_app.database import get_db
from web_app.models.backups import Backups

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery("tasks", broker="redis://localhost:6379/0")

@celery.task
async def send_reserve_copies(email: str, db: AsyncSession = Depends(get_db)):
    excel_file = generate_excel_report(db)
    today = datetime.now().date()

    # Find all reserve copies that need to be sent today
    stmt = select(Backups).where(Backups.send_date == today)
    result = await db.execute(stmt)
    reserve_copies = result.scalars().all()

    for reserve_copy in reserve_copies:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
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
            await server.send_message(msg)

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

        await db.commit()

    # Очищаем BytesIO объект
    excel_file.close()