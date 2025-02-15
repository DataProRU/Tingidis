from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import date

from web_app.schemas.objects import ObjectResponse
from web_app.schemas.users import UserResponse
from web_app.schemas.customers import CustomerResponse


class ContractsGetResponse(BaseModel):
    id: Optional[int] = None
    name: str
    customer: CustomerResponse
    executor: UserResponse
    code: ObjectResponse
    number: str
    sign_date: date
    price: float
    theme: str
    evolution: Optional[str] = None
    agreements: List["AgreementsResponse"]

    class Config:
        orm_mode = True


class ContractsCreateResponse(BaseModel):
    code: int
    name: str
    customer: int
    executor: int
    number: str
    sign_date: Optional[date] = None
    price: float
    theme: str
    evolution: Optional[str] = None

    class Config:
        orm_mode = True


class ContractsResponse(BaseModel):
    id: Optional[int] = None
    code: int
    name: str
    customer: int
    executor: int
    number: str
    sign_date: date
    price: float
    theme: str
    evolution: Optional[str] = None

    class Config:
        orm_mode = True


class ContractsUpdate(BaseModel):
    code: Optional[int] = None
    name: Optional[constr(max_length=50)] = None
    customer: Optional[int] = None
    executor: Optional[int] = None
    number: Optional[constr(max_length=256)] = None
    sign_date: Optional[date] = None
    price: Optional[float] = None
    theme: Optional[constr(max_length=50)] = None
    evolution: Optional[constr(max_length=30)] = None


# Отложенный импорт
from web_app.schemas.agreements import AgreementsResponse

ContractsGetResponse.update_forward_refs()
