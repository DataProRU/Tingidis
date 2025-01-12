# Фикстура для создания асинхронного движка
import os
from typing import Generator, Any

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from starlette.testclient import TestClient

from web_app.database import get_db
from web_app.main import app

CLEAN_TABLES = [
    "users",
]

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", "postgresql+asyncpg://admin:2606QWmg@localhost:5433/tests"
)

@pytest.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)
    yield engine

@pytest.fixture(scope="session")
async def async_session_test(async_engine):

    async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
    yield async_session



@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test, async_engine):
    TestBase = declarative_base()
    async with async_engine.begin() as conn:
        await conn.run_sync(TestBase.metadata.create_all)
    """Clean data in all tables before running test function"""
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(text(f"TRUNCATE TABLE {table_for_cleaning};"))





async def _get_test_db():
    try:
        # create async engine for interaction with database
        test_engine = create_async_engine(
            TEST_DATABASE_URL, future=True, echo=True
        )

        # create session for the interaction with database
        test_async_session = sessionmaker(
            test_engine, expire_on_commit=False, class_=AsyncSession
        )
        yield test_async_session()
    finally:
        pass


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client

# @pytest.fixture
# async def async_engine():
#     engine = create_async_engine(
#         "sqlite+aiosqlite:///:memory:"
#     )  # In-memory база данных
#     yield engine
#     await engine.dispose()




# # Фикстура для фабрики сессий
# @pytest.fixture
# async def session_factory(async_engine):
#     return async_sessionmaker(bind=async_engine, expire_on_commit=False)
#
#
# # Фикстура для подключения к базе данных
# @pytest.fixture
# async def db(session_factory) -> AsyncSession:
#     async with session_factory() as session:
#         yield session
#
#
# # Фикстура для инициализации базы данных (создает и удаляет таблицы для каждого теста)
# @pytest.fixture(autouse=True)
# async def init_db(async_engine):
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)