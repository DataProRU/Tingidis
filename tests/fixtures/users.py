from datetime import date

import pytest

from web_app.database import WebUser
from web_app.routes.auth_routes import pwd_context

@pytest.fixture
async def sample_user(async_session_test):
    async with async_session_test() as db:
        # Создаем нового пользователя
        new_user = WebUser(
            username="user",
            last_name="Ivan",
            first_name="Ivanov",
            full_name="Ivan Ivanovich",
            middle_name="Ivanovich",
            position="Engineer",
            phone="+7 (911) 481 00 52",
            email="ivanov@mail.com",
            telegram="@ivan",
            birthdate=date(2024, 1, 1),
            category="test user",
            specialization="Engineering",
            notes="test user",
            login="user",
            password=pwd_context.hash("123456789"),  # Обязательно хэшируйте пароли в реальном коде!
            role="user",
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
