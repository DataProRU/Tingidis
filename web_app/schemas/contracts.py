from pydantic import BaseModel, Field, constr
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship
from web_app.database import Base
from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Text,
    create_engine,
    ForeignKey,
    DateTime,
    DECIMAL as Decimal,
)


class ContractsModel(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(Integer, ForeignKey("objects.id"), nullable=False)
    name = Column(String(50), nullable=False)

    number = Column(String(256), nullable=False, unique=True)
    sign_date = Column(DateTime, nullable=False, default=func.now())
    price = Column(Decimal, nullable=False)
    theme = Column(String(50), nullable=False)
    evolution = Column(String(30), nullable=False, default="Создан")


""""
class ContractCreate(BaseModel):
    code: int
    name: constr(max_length=50)
    customer: int
    executor: int
    number: constr(max_length=256)
    sign_date: Optional[datetime] = Field(default_factory=datetime.now)
    price: float
    theme: constr(max_length=50)
    evolution: constr(max_length=30)


class ContractUpdate(BaseModel):
    code: Optional[int] = None
    name: Optional[constr(max_length=50)] = None
    customer: Optional[int] = None
    executor: Optional[int] = None
    number: Optional[constr(max_length=256)] = None
    sign_date: Optional[datetime] = None
    price: Optional[float] = None
    theme: Optional[constr(max_length=50)] = None
    evolution: Optional[constr(max_length=30)] = None """
