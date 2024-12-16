import pytest
from web_app.database import async_session
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
    return Jinja2Templates(directory="web_app/templates")
