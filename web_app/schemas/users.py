from pydantic import BaseModel
from sqlalchemy.testing.fixtures import TestBase
from web_app.database import Base
from sqlalchemy import Column, Integer, String, Date, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import date


class WebUser(Base, TestBase):
    __tablename__ = "web_user"

    id = Column(Integer, primary_key=True, autoincrement=True)

    first_name = Column(String, unique=True, nullable=False)
    last_name = Column(String, nullable=False)
    father_name = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    position = Column(String, nullable=True)
    phone = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True, nullable=False, index=True)
    telegram = Column(String, unique=True, nullable=True)
    birthday = Column(Date, nullable=True)
    category = Column(String, nullable=True)
    specialization = Column(String, nullable=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    role = Column(String, nullable=False, server_default="user")

    tokens = relationship(
        "TokenSchema", back_populates="user", cascade="all, delete-orphan"
    )


class WebUserResponse(BaseModel):

    first_name: str
    last_name: str
    father_name: str
    full_name: str
    position: str
    phone: str
    email: str
    telegram: str
    birthday: date
    category: str
    specialization: str
    username: str
    password: str
    notes: str
    role: str


class WebUserCreate(BaseModel):

    first_name: str
    last_name: str
    father_name: str
    full_name: str
    position: str
    phone: str
    email: str
    telegram: str
    birthday: date
    category: str
    specialization: str
    username: str
    password: str
    notes: str
    role: str


# Модель запроса для регистрации
class UserCreate(BaseModel):
    username: str
    password: str
    role: str


# Модель запроса для входа
class UserLogin(BaseModel):
    username: str
    password: str
