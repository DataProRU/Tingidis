from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import declarative_base, relationship  # Updated import
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Строка подключения к базе данных
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://admin:2606QWmg@localhost:5432/users"
)

async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

# Создаем базовый класс для моделей
Base = declarative_base()  # Now uses sqlalchemy.orm.declarative_base


# Асинхронная функция для создания таблиц
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with async_session() as session:
        yield session
