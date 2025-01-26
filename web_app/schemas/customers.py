from pydantic import BaseModel, constr
from typing import Optional


class CustomerCreate(BaseModel):
    name: constr(min_length=1)
    address: Optional[str] = None
    inn: Optional[str] = None


class CustomerResponse(BaseModel):
    id: int

    name: str
    address: str
    inn: str


class CustomerUpdate(BaseModel):
    name: Optional[constr(min_length=1)] = None
    address: Optional[str] = None
    inn: Optional[str] = None
