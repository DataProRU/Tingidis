# Фикстура для создания асинхронного движка
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from web_app.database import Base


@pytest.fixture
async def async_engine():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:"
    )  # In-memory база данных
    yield engine
    await engine.dispose()


# Фикстура для фабрики сессий
@pytest.fixture
async def session_factory(async_engine):
    return async_sessionmaker(bind=async_engine, expire_on_commit=False)


# Фикстура для подключения к базе данных
@pytest.fixture
async def db(session_factory) -> AsyncSession:
    async with session_factory() as session:
        yield session


# Фикстура для инициализации базы данных (создает и удаляет таблицы для каждого теста)
@pytest.fixture(autouse=True)
async def init_db(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)