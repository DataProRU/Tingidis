from pydantic import BaseModel, Field, constr
from datetime import datetime, date
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL as Decimal
from sqlalchemy.sql import func
from web_app.database import Base


class ContractsModel(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(Integer, ForeignKey("objects.id"), nullable=False)
    name = Column(String(50), nullable=False)
    number = Column(String(256), nullable=False, unique=True)
    sign_date = Column(DateTime, nullable=False, default=func.now())
    price = Column(Decimal(precision=10, scale=2), nullable=False)
    theme = Column(String(50), nullable=False)
    evolution = Column(String(30), nullable=False, server_default="Создан")


class ContractCreate(BaseModel):
    code: int
    name: constr(max_length=50)
    number: constr(max_length=256) = Field(..., pattern=r"^\d{1,256}$")
    sign_date: date = Field(default_factory=datetime.now)
    price: float
    theme: constr(max_length=50)
    evolution: constr(max_length=30)


class ContractUpdate(BaseModel):
    code: Optional[int]
    name: Optional[constr(max_length=50)]
    number: Optional[constr(max_length=256)] = Field(None, pattern=r"^\d{1,256}$")
    sign_date: Optional[date]
    price: Optional[float]
    theme: Optional[constr(max_length=50)]
    evolution: Optional[constr(max_length=30)]


class ContractResponse(BaseModel):
    id: int
    code: int
    name: str
    number: str
    sign_date: date  # Ensure this matches the SQLAlchemy model
    price: float  # Ensure this matches the SQLAlchemy model
    theme: str
    evolution: str
