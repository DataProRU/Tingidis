from pydantic import BaseModel
from pydantic import Field, constr
from typing import Optional
from datetime import date


# Schema
class BusinessContractsCreate(BaseModel):
    code: int
    name: constr(max_length=50)
    customer: int
    executor: int
    number: constr(max_length=256)
    sign_date: Optional[date] = None
    price: float
    theme: constr(max_length=50)
    evolution: constr(max_length=30) = "Создан"

    class Config:
        orm_mode = True

class BusinessContractsResponse(BaseModel):
    id: int
    code: int
    name: str
    customer: int
    executor: int
    number: str
    sign_date: date
    price: float
    theme: str
    evolution: str

    class Config:
        orm_mode = True
