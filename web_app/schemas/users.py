from pydantic import BaseModel
from sqlalchemy.testing.fixtures import TestBase
from web_app.database import Base
from sqlalchemy import Column, Integer, String, Date, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


class WebUser(Base, TestBase):
    __tablename__ = "web_user"

    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String, unique=True, nullable=False)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    full_name = Column(String, nullable=False)
    position = Column(String, nullable=True)
    phone = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True, nullable=False, index=True)
    telegram = Column(String, unique=True, nullable=True)
    birthdate = Column(Date, nullable=True)
    category = Column(String, nullable=True)
    specialization = Column(String, nullable=True)
    notes = Column(Text, nullable=True)  # Для длинных текстов
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Здесь требуется хэширование
    role = Column(String, nullable=False, server_default="user")

    tokens = relationship("TokenSchema", back_populates="user")


# Модель запроса для регистрации
class UserCreate(BaseModel):
    username: str
    password: str
    role: str


# Модель запроса для входа
class UserLogin(BaseModel):
    username: str
    password: str
