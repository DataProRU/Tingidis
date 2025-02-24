from fastapi import HTTPException, APIRouter, Depends, status, Response
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta
from web_app.database import get_db
from sqlalchemy.future import select
from web_app.models.backups import Backups
from web_app.schemas.backups import (
    ReserveCopyResponse
)
from web_app.middlewares.auth_middleware import token_verification_dependency
from web_app.utils.utils import log_action
from web_app.utils.reports import generate_excel_report


router = APIRouter()

@router.post("/reserve-copy")
def create_reserve_copy(reserve_copy: ReserveCopyResponse, db: AsyncSession = Depends(get_db)):
    # Calculate send_date based on frequency
    today = datetime.now().date()
    if reserve_copy.frequency == 1:
        send_date = today + timedelta(days=1)
    elif reserve_copy.frequency == 2:
        send_date = today + timedelta(days=7)
    elif reserve_copy.frequency == 3:
        send_date = today + timedelta(days=30)
    elif reserve_copy.frequency == 4:
        send_date = today + timedelta(days=90)
    elif reserve_copy.frequency == 5:
        send_date = today + timedelta(days=180)
    elif reserve_copy.frequency == 6:
        send_date = today + timedelta(days=360)

    db_reserve_copy = Backups(email=reserve_copy.email, frequency=reserve_copy.frequency, send_date=send_date)
    db.add(db_reserve_copy)
    db.commit()
    db.refresh(db_reserve_copy)

    return db_reserve_copy


@router.get("/reserve-copy", response_model=List[ReserveCopyResponse])
async def get_reserve_copies(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    stmt = select(Backups)
    result = await db.execute(stmt)
    reserve_copies = result.scalars().all()
    return reserve_copies


@router.get("/export", response_class=Response)
async def export_to_excel(
    db: AsyncSession = Depends(get_db),
    # user_data: dict = Depends(token_verification_dependency),
):
    # Генерируем Excel-файл
    excel_file = await generate_excel_report(db)

    # Возвращаем файл как ответ
    headers = {"Content-Disposition": 'attachment; filename="report.xlsx"'}

    return Response(
        content=excel_file.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )
