from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from web_app.database import get_db
from fastapi import HTTPException, APIRouter, Depends, status
from web_app.models.project_statuses import ProjectStatuses


async def add_initial_project_statuses(db: AsyncSession = Depends(get_db)):
    statuses = [
        "Разработка",
        "Выдано",
        "В экспертизе",
        "Ожидание ИД",
        "Ожидание Аванса",
    ]

    stmt = select(ProjectStatuses)
    result = await db.execute(stmt)
    project_statuses = result.scalars().all()

    existing_projects = {status.name for status in project_statuses}

    for status_name in statuses:
        if status_name not in existing_projects:
            db.add(ProjectStatuses(name=status_name))

    await db.commit()
