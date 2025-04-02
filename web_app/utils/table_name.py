from datetime import datetime

from sqlalchemy import select, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from web_app.schemas.personal_settings import SettingsResponse, SettingsData


async def create_default_settings(
    table, component: str, db: AsyncSession
) -> SettingsResponse:
    """Создает настройки по умолчанию для всех колонок таблицы"""
    default_columns = {}

    for column in table.table.columns:
        column_name = column.name
        # Получаем уникальные значения для колонки
        try:
            column_attr = getattr(table, column_name)
            stmt = select(distinct(column_attr)).where(column_attr is not None)
            result = await db.execute(stmt)
            unique_values = result.scalars().all()
        except Exception as e:
            unique_values = []

        default_columns[column_name] = {
            "width": 200,  # дефолтная ширина
            "title": None,  # дефолтный заголовок
            "filters_checkbox": unique_values,  # все уникальные значения
            "visible": True,
        }

    settings_data = SettingsData(columns=default_columns, filters={})

    return SettingsResponse(
        component=component,
        settings=settings_data,
        user_id=1,
        updated_at=datetime.utcnow(),
    )
