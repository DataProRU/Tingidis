import pytest
from services.auth_service import login_user, register_user
from database import async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates


@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def db_session():
    async with async_session() as session:
        yield session


@pytest.fixture(scope="module")
def templates():
    # Mock templates if needed
    return Jinja2Templates(directory="templates")
