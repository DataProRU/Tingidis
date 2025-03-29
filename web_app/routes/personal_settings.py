from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from web_app.middlewares.auth_middleware import token_verification_dependency
from web_app.models import PersonalSettings, Users, Projects, ProjectExecutors
from web_app.schemas.personal_settings import SettingsData, SettingsResponse
from web_app.database import get_db
from web_app.services.default_settings import create_default_settings
from web_app.services.get_data_from_fk_columns import get_unique_values
from web_app.utils.table_name import get_table_by_component

router = APIRouter(prefix="/api/user-settings", tags=["User Settings"])


@router.get("/{component}", response_model=SettingsResponse)
async def get_settings(
    component: Any,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(token_verification_dependency),
):
    print(current_user, "!!!!!!!!!!!!!!!!")

    table = await get_table_by_component(component)
    if table is None:
        raise HTTPException(
            status_code=404, detail=f"Component '{component}' not found"
        )

    result = await db.execute(
        select(PersonalSettings).where(
            PersonalSettings.user_id == current_user["id"],
            PersonalSettings.component == component,
        )
    )

    personal_settings = result.scalars().one_or_none()

    if not personal_settings:
        default_settings = await create_default_settings(
            table, component, db, current_user["id"]
        )
        return default_settings

    settings_dict = personal_settings.settings.copy()

    if "columns" in settings_dict:
        valid_columns = {}

        for column_name, column_settings in settings_dict["columns"].items():
            try:
                column_attr = getattr(table, column_name)
                valid_columns[column_name] = column_settings.copy()
                if not column_settings.get(
                    "visible", True
                ):  # По умолчанию visible=True
                    continue  # Пропускаем невидимые столбцы

                if "filters_checkbox" in column_settings:
                    unique_values = await get_unique_values(db, table, column_name)
                    valid_columns[column_name]["filters_checkbox"] = unique_values

            except AttributeError:
                continue

        # -------- ОТДЕЛЬНЫЕ ПРОВЕРКИ ДЛЯ ВСТАВКИ ДАННЫХ В СТОЛБЦЫ - Доп ответственные в Projects - Контактные данные в Customers - Доп соглашения в Contracts
        if component == "projects" and "project_executor" not in valid_columns:
            stmt = (
                select(distinct(Users.full_name))
                .select_from(Projects)
                .join(ProjectExecutors, Projects.project_executors)
                .join(Users, ProjectExecutors.user_info)
                .where(Users.full_name.isnot(None))
            )

            result = await db.execute(stmt)
            unique_values = result.scalars().all()

            valid_columns["project_executor"] = settings_dict["columns"][
                "project_executor"
            ]
            valid_columns["project_executor"]["filters_checkbox"] = unique_values

        elif component == "customers" and "contacts_" not in valid_columns:
            valid_columns["contacts_"] = settings_dict["columns"]["contacts_"]

        elif component == "contracts" and "agreements_" not in valid_columns:
            valid_columns["agreements_"] = settings_dict["columns"]["agreements_"]
        # -------- ОТДЕЛЬНЫЕ ПРОВЕРКИ ДЛЯ ВСТАВКИ ДАННЫХ В СТОЛБЦЫ - Доп ответственные в Projects - Контактные данные в Customers - Доп соглашения в Contracts

        if "operation" not in valid_columns:
            valid_columns["operation"] = settings_dict["columns"]["operation"]

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

    if settings_dict.get("sort") is not None:
        if settings_dict["sort"].get("direction"):
            direction = settings_dict["sort"]["direction"].lower()
            if direction not in ("asc", "desc"):
                raise HTTPException(
                    status_code=400,
                    detail="Sort direction must be either 'asc' or 'desc'",
                )
            settings_dict["sort"]["direction"] = direction

    if "columns" in settings_dict:
        for col_settings in settings_dict["columns"].values():
            col_settings["visible"] = col_settings.get("visible", True)
            col_settings["filters_checkbox"] = None

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
            user_id=current_user.get("id"),
            component=component,
            settings=settings_dict,
            updated_at=datetime.utcnow(),
        )
        db.add(existing)

    await db.commit()
    await db.refresh(existing)

    return existing
