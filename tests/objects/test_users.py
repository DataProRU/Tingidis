import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from passlib.context import CryptContext
from web_app.database import WebUser, TokenSchema
from web_app.routes.auth_routes import router

# Создаем экземпляр приложения FastAPI
app = FastAPI()
app.include_router(router)

# Фикстура для клиента
@pytest.fixture
def client():
    return TestClient(app)

# Фикстура для мокирования базы данных
@pytest.fixture
def mock_db_session():
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session
    with patch('web_app.routes.auth_routes.async_session', return_value=mock_session):
        yield mock_session

# Фикстура для мокирования сервисов
@pytest.fixture
def mock_auth_service():
    with patch('web_app.services.auth_service.create_token', new_callable=AsyncMock) as mock_create_token, \
         patch('web_app.services.auth_service.save_token', new_callable=AsyncMock) as mock_save_token, \
         patch('web_app.services.auth_service.validate_refresh_token', new_callable=AsyncMock) as mock_validate_refresh_token, \
         patch('web_app.services.auth_service.remove_token', new_callable=AsyncMock) as mock_remove_token:
        yield {
            'create_token': mock_create_token,
            'save_token': mock_save_token,
            'validate_refresh_token': mock_validate_refresh_token,
            'remove_token': mock_remove_token,
        }

# Тесты регистрации пользователя
@pytest.mark.asyncio
async def test_register_user(client, mock_db_session, mock_auth_service):
    mock_db_session.execute.return_value.scalar_one_or_none.return_value = None
    user_data = {"username": "testuser", "password": "testpassword", "role": "user"}
    response = await client.post("/register", json=user_data)
    assert response.status_code == 200

# Тесты входа
@pytest.mark.asyncio
async def test_login_user(client, mock_db_session, mock_auth_service):
    mock_db_session.execute.return_value.scalar_one_or_none.return_value = WebUser(
        id=1,
        username="testuser",
        password=CryptContext(schemes=["bcrypt"]).hash("testpassword"),
        role="user"
    )
    response = await client.post("/login", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200

# Тесты обновления токена
@pytest.mark.asyncio
async def test_refresh_token(client, mock_auth_service):
    mock_auth_service['validate_refresh_token'].return_value = {"sub": "testuser", "role": "user"}
    response = await client.get("/refresh", cookies={"refresh_token": "mock_refresh_token"})
    assert response.status_code == 200

# Тесты выхода
@pytest.mark.asyncio
async def test_logout_user(client, mock_auth_service):
    response = await client.post("/logout", cookies={"refresh_token": "mock_refresh_token"})
    assert response.status_code == 200

# Тесты получения токенов
@pytest.mark.asyncio
async def test_get_all_tokens(client, mock_db_session):
    mock_db_session.execute.return_value.scalars.return_value.all.return_value = [
        TokenSchema(id=1, user_id=1, refresh_token="mock_refresh_token")
    ]
    response = await client.get("/tokens")
    assert response.status_code == 200
