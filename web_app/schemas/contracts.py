"""from pydantic import BaseModel, Field, constr
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
"""

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
