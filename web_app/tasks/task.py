from celery import Celery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
from fastapi import Depends
from web_app.database import get_db
from web_app.models.backups import Backups

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
async def send_reserve_copies():
    async with get_db() as db:
        today = datetime.now().date()

        # Find all reserve copies that need to be sent today
        stmt = select(Backups).where(Backups.send_date == today)
        result = await db.execute(stmt)
        reserve_copies = result.scalars().all()

        for reserve_copy in reserve_copies:
            # Send the reserve copy (mock implementation)
            print(f"Sending reserve copy to {reserve_copy.email}")

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