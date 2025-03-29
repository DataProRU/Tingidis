from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from web_app.models import PersonalSettings
from web_app.schemas.personal_settings import SettingsData, SettingsResponse
from web_app.database import get_db

router = APIRouter(prefix="/api/user-settings", tags=["User Settings"])


@router.get("/{component}", response_model=SettingsResponse)
async def get_settings(
        component: Any,
        db: Session = Depends(get_db),
        #current_user: dict = Depends(get_current_user)
):
    personal_settings = db.query(PersonalSettings).filter(
        PersonalSettings.user_id == 1,
        PersonalSettings.component == component
    ).first()

    if not personal_settings:
        empty_settings = SettingsData()
        return SettingsResponse(
            component=component,
            settings=empty_settings,
            user_id=1,
            updated_at=datetime.utcnow()
        )

    return personal_settings


@router.post("/", response_model=SettingsResponse)
async def update_settings(
        component: str,
        settings_data: SettingsData,
        db: Session = Depends(get_db),
        #current_user: dict = Depends(get_current_user)
):

    existing = db.query(PersonalSettings).filter(
        PersonalSettings.user_id == 1,
        PersonalSettings.component == component
    ).first()


    settings_dict = settings_data.model_dump(exclude_unset=True)

    if existing:
        existing.settings = settings_dict
        existing.updated_at = datetime.utcnow()
    else:
        existing = PersonalSettings(
            user_id=1,
            component=component,
            settings=settings_dict,
            updated_at=datetime.now()
        )
        db.add(existing)

    db.commit()
    db.refresh(existing)

    return existing