import logging
from datetime import datetime, time, timedelta

from apscheduler.triggers.date import DateTrigger
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from web_app.database import get_db
from web_app.models import Backups
from web_app.services.email import send_email_with_excel_and_dump
from web_app.services.scheduler import scheduler
from web_app.utils.reports import generate_excel_report

logger = logging.getLogger(__name__)


async def restore_scheduled_tasks(db: AsyncSession = Depends(get_db)):
    tomorrow = (datetime.now() + timedelta(days=1)).date()
    send_date = datetime.combine(tomorrow, time(hour=10, minute=0))
    job_id = f"backup_{send_date}"

    existing_job = scheduler.get_job(job_id)
    if existing_job:
        logger.info(f"Задача для отправки отчета на {send_date} уже существует.")
        return

    excel_report = await generate_excel_report(db)

    scheduler.add_job(
        send_email_with_excel_and_dump,
        trigger=DateTrigger(run_date=send_date),
        args=(excel_report, db),
        id=job_id,
    )
    logger.info(f"Восстановлена задача для отправки отчета на {send_date}.")
