import logging
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from io import BytesIO
from datetime import datetime, timedelta

from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from web_app.models import Backups
from web_app.services.backup import create_database_dump, copy_dump_from_container


logger = logging.getLogger(__name__)
load_dotenv()

# SMTP настройки
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")


async def send_email_with_excel_and_dump(excel_file: BytesIO, db: AsyncSession):
    from web_app.services.scheduler import schedule_report_sending

    today = datetime.now().date()
    today_date = datetime.now().strftime("%d.%m.%Y")

    result = await db.execute(select(Backups).where(Backups.send_date == today))
    backups = result.scalars().all()
    emails = [backup.email for backup in backups]

    container_name = "postgres_db"
    db_user = DB_USER
    db_name = DB_NAME
    container_dump_path = "/tmp/dump.sql"
    local_dump_file = "./dump.sql"

    try:
        create_database_dump(container_name, db_user, db_name, container_dump_path)

        copy_dump_from_container(container_name, container_dump_path, local_dump_file)

        with open(local_dump_file, "rb") as f:
            dump_data = f.read()

        for email in emails:
            msg = MIMEMultipart()
            msg["From"] = SMTP_USER
            msg["To"] = email
            msg["Subject"] = f"Tingidis - отчет и резервная копия за {today_date}"

            excel_part = MIMEBase("application", "octet-stream")
            excel_part.set_payload(excel_file.read())
            encoders.encode_base64(excel_part)
            excel_part.add_header(
                "Content-Disposition", 'attachment; filename="report.xlsx"'
            )
            msg.attach(excel_part)

            dump_part = MIMEBase("application", "octet-stream")
            dump_part.set_payload(dump_data)
            encoders.encode_base64(dump_part)
            dump_part.add_header(
                "Content-Disposition", 'attachment; filename="dump.sql"'
            )
            msg.attach(dump_part)

            with smtplib.SMTP_SSL(SMTP_HOST, int(SMTP_PORT)) as server:
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(msg)
            logger.info(f"Письмо успешно отправлено на {email}")

            result = await db.execute(select(Backups).where(Backups.email == email))
            backup = result.scalars().first()

            if backup:
                today = datetime.now().date()
                if backup.frequency == 1:
                    new_send_date = today + timedelta(days=1)
                elif backup.frequency == 2:
                    new_send_date = today + timedelta(days=7)
                elif backup.frequency == 3:
                    new_send_date = today + timedelta(days=30)
                elif backup.frequency == 4:
                    new_send_date = today + timedelta(days=90)
                elif backup.frequency == 5:
                    new_send_date = today + timedelta(days=180)
                elif backup.frequency == 6:
                    new_send_date = today + timedelta(days=365)

                backup.send_date = new_send_date

                logger.info(
                    f"Задана новая дата для отправки отчета на почту {email} - {new_send_date}"
                )
                await db.commit()

        await schedule_report_sending(db)

    except Exception as e:
        logger.error(f"Ошибка при отправке письма: {e}")
    finally:
        if os.path.exists(local_dump_file):
            os.remove(local_dump_file)
