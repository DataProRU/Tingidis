from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from web_app.middlewares.auth_middleware import token_verification_dependency
from web_app.models import PersonalSettings
from web_app.schemas.personal_settings import SettingsData, SettingsResponse
from web_app.database import get_db
from web_app.utils.table_name import get_table_by_component

router = APIRouter(prefix="/api/user-settings", tags=["User Settings"])


@router.get("/{component}", response_model=SettingsResponse)
async def get_settings(
    component: Any,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(PersonalSettings).where(
            PersonalSettings.user_id == current_user.get("id"),
            PersonalSettings.component == component,
        )
    )

    personal_settings = result.scalars().one_or_none()

    # если настроек не было в бд, делаем их пустыми
    if not personal_settings:
        empty_settings = SettingsData()
        return SettingsResponse(
            component=component,
            settings=empty_settings,
            user_id=current_user.get("id"),
            updated_at=datetime.utcnow(),
        )

    table = await get_table_by_component(component)
    if table is None:
        return personal_settings

    # получаем json настроек для таблицы в виде:
    """
    {
      "columns": {
        "id": {
          "width": 200,
          "visible": true,
          "title": "Номер"
        },
        "code": {
          "width": 200,
          "visible": true,
          "title": "Шифр",
          "filters": [все значения уникальные из этого столбца - 'code']
        },
        "name": {
          "width": 200,
          "visible": true,
          "title": "ID_имя_объекта",
          "filters": [все значения уникальные из этого столбца - 'name']
        },
        "comment": {
          "width": 200,
          "visible": false,
          "title": "Комментарий"
        },
        "operation": {
          "width": 200,
          "visible": false,
          "title": "Действия"
        }
      },
      "filters": {}
    }
    """

    settings_dict = personal_settings.settings.copy()

    if "columns" in settings_dict:
        valid_columns = {}

        for column_name, column_settings in settings_dict["columns"].items():
            try:
                column_attr = getattr(table, column_name)
                valid_columns[column_name] = column_settings.copy()

                if "filters_all_data_in_column" in column_settings:
                    stmt = select(distinct(column_attr)).where(column_attr != None)
                    result = await db.execute(stmt)
                    unique_values = result.scalars().all()
                    valid_columns[column_name][
                        "filters_all_data_in_column"
                    ] = unique_values
            except AttributeError:
                continue

        settings_dict["columns"] = valid_columns

    personal_settings.settings = settings_dict

    return personal_settings


@router.post("/{component}", response_model=SettingsResponse)
async def update_settings(
    component: str,
    settings_data: SettingsData,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(token_verification_dependency),
):
    settings_dict = settings_data.model_dump(exclude_unset=True)

    if "columns" in settings_dict:
        for col_settings in settings_dict["columns"].values():
            col_settings["filters_all_data_in_column"] = None

    result = await db.execute(
        select(PersonalSettings).where(
            PersonalSettings.user_id == current_user.get("id"),
            PersonalSettings.component == component,
        )
    )

    existing = result.scalar_one_or_none()

    if existing:
        existing.settings = settings_dict
        existing.updated_at = datetime.utcnow()
    else:
        existing = PersonalSettings(
            user_id=1,
            component=component,
            settings=settings_dict,
            updated_at=datetime.utcnow(),
        )
        db.add(existing)

    await db.commit()
    await db.refresh(existing)

    return existing
