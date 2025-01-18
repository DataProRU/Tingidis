from pydantic import BaseModel, constr
from typing import Optional
from sqlalchemy import Column, Integer, String
from web_app.database import Base


class CustomerModel(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)  # строка, не пустое
    address = Column(String)  # строка, может быть пустым
    inn = Column(String)  # строка, может быть пустым


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
