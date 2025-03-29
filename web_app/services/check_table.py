from sqlalchemy import select, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from web_app.models import Projects, ProjectExecutors, Users


async def check_table(component: str, db: AsyncSession):
    default_columns = {}
    if component == "contracts":
        default_columns["agreements_"] = {
            "width": 200,
            "title": "Доп соглашения",
            "filters_checkbox": None,
            "visible": True,
        }

    elif component == "customers":
        default_columns["contacts_"] = {
            "width": 200,
            "title": "Контактные данные",
            "filters_checkbox": None,
            "visible": True,
        }

    elif component == "projects":
        stmt = (
            select(distinct(Users.full_name))
            .select_from(Projects)
            .join(ProjectExecutors, Projects.project_executors)
            .join(Users, ProjectExecutors.user_info)
            .where(Users.full_name.isnot(None))
        )

        result = await db.execute(stmt)
        unique_values = result.scalars().all()

        default_columns["project_executor"] = {
            "width": 200,
            "title": "Доп ответственные",
            "filters_checkbox": unique_values,
            "visible": True,
        }

    return default_columns
