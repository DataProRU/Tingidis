from datetime import datetime, timedelta
from http.client import HTTPException
from typing import List
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from web_app.database import get_db
from web_app.middlewares.auth_middleware import token_verification_dependency
from web_app.models import Backups
from sqlalchemy.future import select

from web_app.schemas.backups import ReserveCopyResponse
from web_app.utils.reports import generate_excel_report


router = APIRouter()


@router.get("/export", response_class=Response)
async def export_to_excel(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
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


@router.post("/reserve-copies", status_code=status.HTTP_201_CREATED)
async def create_reserve_copy(
    reserve_copy: ReserveCopyResponse,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    try:
        result = await db.execute(
            select(Backups).where(Backups.email == reserve_copy.email)
        )
        existing_record = result.scalars().first()

        today = datetime.now().date()
        send_date = today

        if reserve_copy.frequency == 1:
            send_date += timedelta(days=1)
        elif reserve_copy.frequency == 2:
            send_date += timedelta(days=7)
        elif reserve_copy.frequency == 3:
            send_date += timedelta(days=30)
        elif reserve_copy.frequency == 4:
            send_date += timedelta(days=90)
        elif reserve_copy.frequency == 5:
            send_date += timedelta(days=180)
        elif reserve_copy.frequency == 6:
            send_date += timedelta(days=365)

        if existing_record:
            existing_record.frequency = reserve_copy.frequency
            existing_record.send_date = send_date
        else:
            db_reserve_copy = Backups(
                email=reserve_copy.email,
                frequency=reserve_copy.frequency,
                send_date=send_date,
            )
            db.add(db_reserve_copy)

        await db.commit()

        if existing_record:
            await db.refresh(existing_record)
            return existing_record
        else:
            await db.refresh(db_reserve_copy)
            return db_reserve_copy
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/reserve-copies", response_model=List[ReserveCopyResponse])
async def get_reserve_copies(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    stmt = select(Backups)
    result = await db.execute(stmt)
    reserve_copies = result.scalars().all()
    return reserve_copies
