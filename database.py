from fastapi import APIRouter, Request, Depends
from sqlalchemy import Column, Integer, String, Date, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi.templating import Jinja2Templates

import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Строка подключения к базе данных
DATABASE_URL = os.getenv("DATABASE_URL")
async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

# Создаем базовый класс для моделей
Base = declarative_base()


# Определение модели WebUser с использованием SQLAlchemy
class WebUser(Base):
    __tablename__ = "web_user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    last_name = Column(String, unique=True, nullable=False)
    first_name = Column(String, unique=True, nullable=False)
    middle_name = Column(String, unique=True, nullable=False)
    full_name = Column(String, unique=True, nullable=False)
    position = Column(String, unique=True, nullable=False)
    phone = Column(Integer, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    telegram = Column(String, unique=True, nullable=False)
    birthdate = Column(Date, unique=True, nullable=False)
    category = Column(String, unique=True, nullable=False)
    specialization = Column(String, unique=True, nullable=False)
    notes = Column(String, unique=True, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, server_default="user")


# Асинхронная функция для создания таблиц
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with async_session() as session:
        yield session


# Example route to test the database connection
@router.get("/")
async def read_root(db: AsyncSession = Depends(get_db)):
    return {"message": "Database connection is working"}
