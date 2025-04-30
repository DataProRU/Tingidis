from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    DeclarativeBase,
)  # Updated import
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from fastapi.templating import Jinja2Templates
import os

from web_app.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Строка подключения к базе данных
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


# Создаем базовый класс для моделей
class Base(DeclarativeBase):
    pass


# Асинхронная функция для создания таблиц
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with async_session() as session:
        yield session
