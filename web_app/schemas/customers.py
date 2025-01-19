from pydantic import BaseModel, constr
from typing import Optional


class CustomerCreate(BaseModel):
    name: constr(min_length=1)  # строка, не пустое
    address: Optional[str] = None  # строка, может быть пустым
    inn: Optional[str] = None  # строка, может быть пустым


class CustomerResponse(BaseModel):
    id: int

    name: str
    address: str
    inn: str


class CustomerUpdate(BaseModel):
    name: Optional[constr(min_length=1)] = (
        None  # строка, не пустое (если предоставлено)
    )
    address: Optional[str] = None  # строка, может быть пустым
    inn: Optional[str] = None  # строка, может быть пустым
