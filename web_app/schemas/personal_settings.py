from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime


class ColumnSettings(BaseModel):
    width: Optional[int] = 200
    title: Optional[str] = None
    filters_checkbox: Optional[list] = None
    visible: Optional[bool] = True


class SettingsData(BaseModel):
    columns: Optional[dict[str, ColumnSettings]] = None
    filters: Optional[dict[str, Any]] = None
    sort: Optional[dict[str, Any]] = None


class SettingsResponse(BaseModel):
    component: str
    settings: SettingsData
    user_id: int
    updated_at: datetime

    class Config:
        orm_mode = True
