from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from datetime import date

from web_app.database import get_db
from web_app.models.agreements import Agreements
from web_app.models.projects import Projects
from web_app.models.contracts import Contracts
from web_app.middlewares.auth_middleware import token_verification_dependency

router = APIRouter()


@router.get("/deadlines")
async def get_deadlines(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
    before_date: Optional[date] = Query(None, alias="before_date"),
    after_date: Optional[date] = Query(None, alias="after_date"),
):
    deadlines = []

    # Получаем доп соглашения
    query = select(Agreements).where(Agreements.deadline.isnot(None))
    if before_date:
        query = query.where(Agreements.deadline <= before_date)
    if after_date:
        query = query.where(Agreements.deadline >= after_date)
    agreements = (await db.execute(query)).scalars().all()
    deadlines.extend(
        {"date": a.deadline, "type": 1, "name": a.name} for a in agreements
    )

    # Получаем проекты
    query = select(Projects).where(Projects.deadline.isnot(None))
    if before_date:
        query = query.where(Projects.deadline <= before_date)
    if after_date:
        query = query.where(Projects.deadline >= after_date)
    projects = (await db.execute(query)).scalars().all()
    deadlines.extend({"date": p.deadline, "type": 3, "name": p.name} for p in projects)

    # Сортируем по дате
    deadlines.sort(key=lambda x: x["date"])
    return deadlines
