from fastapi import HTTPException, APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from web_app.database import get_db
from sqlalchemy.future import select
from web_app.models.backups import Backups
from web_app.schemas.backups import (
    ReserveCopyCreate
)
from web_app.middlewares.auth_middleware import token_verification_dependency

from web_app.utils.utils import log_action

router = APIRouter()

@router.post("/reserve-copy/")
def create_reserve_copy(reserve_copy: ReserveCopyCreate):
    db = SessionLocal()

    # Calculate send_date based on frequency
    today = datetime.now().date()
    if reserve_copy.frequency == 1:
        send_date = today + timedelta(days=7)
    elif reserve_copy.frequency == 2:
        send_date = today + timedelta(days=30)
    elif reserve_copy.frequency == 3:
        send_date = today + timedelta(days=90)
    elif reserve_copy.frequency == 4:
        send_date = today + timedelta(days=180)
    elif reserve_copy.frequency == 5:
        send_date = today + timedelta(days=365)

    db_reserve_copy = ReserveCopy(email=reserve_copy.email, frequency=reserve_copy.frequency, send_date=send_date)
    db.add(db_reserve_copy)
    db.commit()
    db.refresh(db_reserve_copy)

    return db_reserve_copy