from datetime import datetime

from sqlalchemy import select, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from web_app.schemas.personal_settings import SettingsResponse, SettingsData
from web_app.services.check_table import check_table
from web_app.services.get_data_from_fk_columns import get_unique_values


async def create_default_settings(
    table, component: str, db: AsyncSession, current_user: int
) -> SettingsResponse:
    """Создает настройки по умолчанию для всех колонок таблицы"""
    default_columns = {}

    for column in table.__table__.columns:
        column_name = column.name
        # Получаем уникальные значения для колонки
        try:
            unique_values = await get_unique_values(db, table, column_name)
        except Exception as e:
            unique_values = []

        default_columns[column_name] = {
            "width": 200,  # дефолтная ширина
            "title": None,  # дефолтный заголовок
            "filters_checkbox": unique_values,  # все уникальные значения
        }

    default_columns |= await check_table(component=component, db=db)

    default_columns["operation"] = {
        "width": 200,
        "title": "Действия",
        "filters_checkbox": None,
        "visible": True,
    }

    settings_data = SettingsData(columns=default_columns, filters=None, sort=None)

    return SettingsResponse(
        component=component,
        settings=settings_data,
        user_id=current_user,
        updated_at=datetime.utcnow(),
    )
