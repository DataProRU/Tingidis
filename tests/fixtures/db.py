# Фикстура для создания асинхронного движка
import asyncio
import os

import pytest
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient
from web_app.database import Base

from web_app.database import get_db
from web_app.main import app
from web_app.services.auth import create_token

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_KEY = os.getenv("REFRESH_KEY")
ALGORITHM = os.getenv("ALGORITHM")

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", "postgresql+asyncpg://admin:2606QWmg@localhost:5433/tests"
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)
    yield engine


@pytest.fixture(scope="session")
async def async_session_test(async_engine):

    async_session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_engine, async_session_test):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def _get_test_db():
    try:
        test_engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)
        test_async_session = sessionmaker(
            test_engine, expire_on_commit=False, class_=AsyncSession
        )
        async with test_async_session() as session:
            yield session
    finally:
        await test_engine.dispose()  # Закрытие движка, если это необходимо


@pytest.fixture(scope="function")
def client(sample_user):
    app.dependency_overrides[get_db] = _get_test_db
    client = TestClient(app)
    token = create_token(
        data={"sub": sample_user.username, "role": sample_user.role},
        key=SECRET_KEY,
        algoritm=ALGORITHM,
    )
    client.headers = {"Authorization": f"Bearer {token}"}
    return client


@pytest.fixture(scope="function")
def admin_client(admin_user):
    app.dependency_overrides[get_db] = _get_test_db
    client = TestClient(app)
    token = create_token(
        data={"sub": admin_user.username, "role": admin_user.role},
        key=SECRET_KEY,
        algoritm=ALGORITHM,
    )
    client.headers = {"Authorization": f"Bearer {token}"}
    return client
