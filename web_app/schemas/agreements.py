from sqlalchemy import Column, Integer, String, Date, Text, create_engine
from pydantic import BaseModel
from web_app.database import Base
from typing import Optional
from datetime import date
from sqlalchemy.orm import declarative_base, relationship
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

from sqlalchemy.sql import func


class AgreementsModel(Base):
    __tablename__ = "agreements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    number = Column(String, nullable=False)
    deadline = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    contract = Column(Integer, ForeignKey("contracts.id"), nullable=False)

    # tokens = relationship(
    #     "ContractsModel", back_populates="user", cascade="all, delete-orphan"
    # )


class AgreementsCreate(BaseModel):
    name: str
    number: str
    deadline: Optional[date] = None
    notes: Optional[str] = None
    contract: int


class AgreementsResponse(BaseModel):
    id: int
    name: str
    number: str
    deadline: date
    notes: Optional[str] = None
    contract: int
