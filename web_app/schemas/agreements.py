from pydantic import BaseModel
from typing import Optional
from datetime import date


class AgreementsCreate(BaseModel):
    name: str
    number: str
    deadline: Optional[date] = None
    notes: Optional[str] = None
    contract: int


class AgreementsResponse(BaseModel):
    id: int
    name: str
    number: str
    deadline: date
    notes: Optional[str] = None
    contract: int
