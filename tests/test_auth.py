import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from web_app.main import app
from web_app.database import async_session


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


@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.anyio
async def test_get_register(client: TestClient):
    response = client.get("/register")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_login(client: TestClient):
    response = client.get("/login")
    assert response.status_code == 200
