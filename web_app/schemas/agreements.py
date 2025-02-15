from pydantic import BaseModel, constr
from typing import Optional
from datetime import date


class AgreementsGetResponse(BaseModel):
    id: Optional[int] = None
    name: str
    number: str
    price: float
    deadline: Optional[date] = None
    notes: Optional[str] = None
    contract: "ContractsResponse"

    class Config:
        orm_mode = True


class AgreementsCreate(BaseModel):
    name: str
    number: str
    price: float
    deadline: Optional[date] = None
    notes: Optional[str] = None
    contract: int


class AgreementsResponse(BaseModel):
    id: Optional[int] = None
    name: Optional[constr(max_length=50)] = None
    number: Optional[constr(max_length=50)] = None
    price: Optional[float] = None
    deadline: Optional[date] = None
    notes: Optional[str] = None
    contract: Optional[int] = None


# Отложенный импорт
from web_app.schemas.contracts import ContractsResponse

AgreementsGetResponse.update_forward_refs()
