from web_app.models.project_statuses import ProjectStatuses
from web_app.database import get_db


async def add_initial_project_statuses():
    statuses = ["разработка", "выдано", "в экспертизе", "ожидание ИД", "ожидание аванса"]

    # Используем async with для получения сессии
    async for db in get_db():
        for status_name in statuses:
            db_status = ProjectStatuses(name=status_name)
            db.add(db_status)
        await db.commit()
        await db.close()
