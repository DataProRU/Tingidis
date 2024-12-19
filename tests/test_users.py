import pytest
from unittest.mock import MagicMock
from datetime import date
from fastapi.responses import RedirectResponse
from fastapi import HTTPException
from web_app.routes.users import add_user  # Функция добавления пользователя
from web_app.database import WebUser  # Импорт модели пользователя
from web_app.database import async_session  # Импорт сессии базы данных


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


# Тестирование добавления пользователя
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
        "birthdate": date(1985, 7, 15),
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
