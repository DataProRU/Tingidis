import pytest
from database import async_session, WebUser
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def db_session():
    async with async_session() as session:
        yield session
