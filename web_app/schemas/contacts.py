from pydantic import BaseModel, constr
from typing import Optional


class ContactGetResponse(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    father_name: str
    phone: str
    email: str
    position: str
    customer: "CustomerResponse"

    class Config:
        orm_mode = True


class ContactCreateResponse(BaseModel):
    first_name: str
    last_name: str
    father_name: str
    phone: str
    email: str
    position: str

    class Config:
        orm_mode = True


class ContactResponse(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    father_name: str
    phone: str
    email: str
    position: str
    customer: int

    class Config:
        orm_mode = True


class ContactUpdate(BaseModel):
    first_name: Optional[constr(min_length=1, max_length=50)] = None
    last_name: Optional[constr(min_length=1, max_length=50)] = None
    father_name: Optional[constr(min_length=1, max_length=50)] = None
    phone: Optional[constr(min_length=1, max_length=50)] = None
    email: Optional[constr(min_length=1, max_length=50)] = None
    position: Optional[constr(min_length=1, max_length=50)] = None
    customer: Optional[int] = None


# Отложенный импорт
from web_app.schemas.customers import CustomerResponse

ContactGetResponse.update_forward_refs()
