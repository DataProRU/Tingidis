import pytest
from fastapi.testclient import TestClient
from main import app
from database import async_engine, async_session
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture(scope="module")
async def db_session():
    async with async_session() as session:
        yield session


@pytest.mark.anyio
async def test_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_custom_route(client: TestClient):
    response = client.get("/customaze")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_auth_route(client: TestClient):
    response = client.get("/login")
    assert response.status_code == 200
