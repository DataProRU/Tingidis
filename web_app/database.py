from fastapi import APIRouter, Request, Depends
from sqlalchemy import Column, Integer, String, Date, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship  # Updated import
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi.templating import Jinja2Templates
from sqlalchemy.testing.fixtures import TestBase
from sqlalchemy.types import Enum
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


# Определение модели WebUser с использованием SQLAlchemy
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


class TokenSchema(Base, TestBase):
    __tablename__ = "token_schema"
    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("web_user.id"), nullable=False)
    refresh_token = Column(String)

    user = relationship("WebUser", back_populates="tokens")


class Contract(Base, TestBase):
    __tablename__ = "contract"
    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_code = Column(Integer, unique=True, nullable=False)
    object_name = Column(String, nullable=False)
    customer = Column(String, nullable=False)
    executer = Column(String, nullable=False)
    contract_number = Column(String, nullable=False)
    status = Column(String, nullable=False)
    stage = Column(String, nullable=False)
    contract_scan = Column(String, nullable=False)
    original_scan = Column(String, nullable=False)
    percent_complite = Column(Integer, nullable=False)
    date_start = Column(Date, nullable=False)
    date_finish = Column(Date)
    cost = Column(Integer)
    money_received = Column(Integer)
    money_left = Column(Integer)
    scan_complited_act = Column(String, nullable=False)
    original_complited_act = Column(String, nullable=False)
    volumes = Column(Text, nullable=False)
    notes = Column(Text, nullable=True)


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
