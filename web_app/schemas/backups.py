from pydantic import BaseModel, validator
from typing import Optional

class ReserveCopyCreate(BaseModel):
    email: str
    frequency: int

    @field_validator('email')
    def email_not_empty(cls, v):
        if not v:
            raise ValueError('Email cannot be empty')
        return v

    @field_validator('frequency')
    def frequency_valid(cls, v):
        if v not in [1, 2, 3, 4, 5]:
            raise ValueError('Frequency must be between 1 and 5')
        return v

    class Config:
        orm_mode = True