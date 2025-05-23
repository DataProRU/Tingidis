from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date


class ReserveCopyResponse(BaseModel):
    id: Optional[int] = None
    email: str
    frequency: int
    send_date: Optional[date] = None

    @field_validator("email")
    def email_not_empty(cls, v):
        if not v:
            raise ValueError("Email cannot be empty")
        return v

    @field_validator("frequency")
    def frequency_valid(cls, v):
        if v not in [1, 2, 3, 4, 5]:
            raise ValueError("Frequency must be between 1 and 5")
        return v

    class Config:
        orm_mode = True
