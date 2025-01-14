from datetime import date

import pytest

from web_app.schemas.users import WebUser
from web_app.routes.auth_routes import pwd_context


@pytest.fixture
async def sample_user(async_session_test):
    async with async_session_test() as db:
        # Создаем нового пользователя
        new_user = WebUser(
            first_name="Ivanov",
            last_name="Ivan",
            father_name="Ivanovich",
            full_name="Ivan Ivanovich",
            position="Engineer",
            phone="+7 (911) 481 00 52",
            email="ivanov@mail.com",
            telegram="@ivan",
            birthday=date(2024, 1, 1),
            category="test user",
            specialization="Engineering",
            username="user",
            password=pwd_context.hash(
                "123456789"
            ),  # Обязательно хэшируйте пароли в реальном коде!
            notes="test user",
            role="user",
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
