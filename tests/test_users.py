import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from fastapi.responses import RedirectResponse
from fastapi import HTTPException
from web_app.main import app  # Импортируйте ваше FastAPI приложение
from web_app.routes.users import add_user  # Функция добавления пользователя


# Мокирование зависимости get_db
@pytest.fixture
def mock_db_session():
    # Мокируем сессию базы данных
    db_session = MagicMock()
    yield db_session
    db_session.close()


# Мокирование токена и request
@pytest.fixture
def mock_request():
    request = MagicMock()
    request.cookies = (
        {}
    )  # Пустой токен (в вашем случае это может быть для теста без аутентификации)
    return request


# Создайте экземпляр TestClient
@pytest.fixture
def client():
    return TestClient(app)


# Тестирование добавления пользователя с неправильной датой
def test_add_user_with_invalid_date(client):
    # Данные для создания нового пользователя с неправильной датой
    data = {
        "last_name": "Ivanov",
        "first_name": "Ivan",
        "middle_name": "Ivanovich",
        "position": "Developer",
        "phone": "+7-800-555-35-35",
        "email": "ivanov@example.com",
        "telegram": "@ivanov",
        "birthdate": "invalid_date",  # Неправильная дата
        "category": "Employee",
        "specialization": "Backend",
        "notes": "Some notes",
        "login": "ivanov_login",
        "password": "SecurePassword123",
        "role": "admin",
    }

    response = client.post("/users/add/", data=data)

    # Проверяем, что ответ содержит ожидаемую ошибку валидации
    assert response.status_code == 422
    assert "detail" in response.json()
    assert any(
        "Input should be a valid date" in error["msg"]
        for error in response.json()["detail"]
    )


# Тестирование добавления пользователя без токена
@pytest.mark.asyncio
async def test_add_user_without_token(mock_db_session, mock_request):
    # Данные для создания нового пользователя
    data = {
        "last_name": "Ivanov",
        "first_name": "Ivan",
        "middle_name": "Ivanovich",
        "position": "Developer",
        "phone": "+7-800-555-35-35",
        "email": "ivanov@example.com",
        "telegram": "@ivanov",
        "birthdate": "1985-07-15",  # Правильная дата
        "category": "Employee",
        "specialization": "Backend",
        "notes": "Some notes",
        "login": "ivanov_login",
        "password": "SecurePassword123",
        "role": "admin",
    }

    # Мы не передаем токен, это имитирует ситуацию, когда токен отсутствует в запросе
    try:
        response = await add_user(
            request=mock_request,
            last_name=data["last_name"],
            first_name=data["first_name"],
            middle_name=data["middle_name"],
            position=data["position"],
            phone=data["phone"],
            email=data["email"],
            telegram=data["telegram"],
            birthdate=data["birthdate"],
            category=data["category"],
            specialization=data["specialization"],
            notes=data["notes"],
            login=data["login"],
            password=data["password"],
            role=data["role"],
            db=mock_db_session,
        )
        # Проверяем, что функция не вызвала исключение и выполнилась без ошибок
        assert isinstance(
            response, RedirectResponse
        )  # Проверяем редирект на другую страницу
        assert response.status_code == 303  # Код состояния для редиректа
    except HTTPException as e:
        # Если мы ожидаем ошибку, например, из-за отсутствия токена
        assert e.status_code == 401  # или другой код ошибки, если не аутентифицировано
