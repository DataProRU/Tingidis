import logging
from datetime import time, datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from sqlalchemy.ext.asyncio import AsyncSession

from web_app.services.email import send_email_with_excel_and_dump
from web_app.utils.reports import generate_excel_report

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()


async def schedule_report_sending(db: AsyncSession):
    tomorrow = (datetime.now() + timedelta(days=1)).date()

    logger.info("Начало добавления события на отправку отчета")

    send_date = datetime.combine(tomorrow, time(hour=10, minute=0))
    job_id = f"backup_{send_date}"

    existing_job = scheduler.get_job(job_id)
    if existing_job:
        logger.warning(f"Задача для отправки отчета на {send_date} уже существует.")
        return

    excel_report = await generate_excel_report(db)

    scheduler.add_job(
        send_email_with_excel_and_dump,
        trigger=DateTrigger(run_date=send_date),
        args=(excel_report, db),
        id=job_id,
    )
    logger.info(f"Запрос на создание отчета был успешно создан на {send_date}")
