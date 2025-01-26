from datetime import date

import pytest

from web_app.models.users import Users
from web_app.routes.auth import pwd_context


@pytest.fixture
async def sample_user(async_session_test):
    async with async_session_test() as db:
        # Создаем нового пользователя
        new_user = Users(
            first_name=None,
            last_name=None,
            father_name=None,
            full_name=None,
            position=None,
            phone=None,
            email=None,
            telegram=None,
            birthday=None,
            category=None,
            specialization=None,
            username="user",
            password=pwd_context.hash(
                "123456789"
            ),  # Обязательно хэшируйте пароли в реальном коде!
            notes=None,
            role="user",
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user


@pytest.fixture
async def another_user(async_session_test):
    async with async_session_test() as db:
        user = Users(
            first_name="Alex",
            last_name="Alexeev",
            father_name="Ivanovich",
            full_name="Alex Ivanovich",
            position="Worker",
            phone="+3 (911) 181 00 32",
            email="alex@mail.com",
            telegram="@alex",
            birthday=date(2001, 2, 2),
            category="test user",
            specialization="Working",
            username="user_alex",
            password=pwd_context.hash(
                "123456789qqFF_"
            ),  # Обязательно хэшируйте пароли в реальном коде!
            notes="another test user",
            role="user",
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user


@pytest.fixture
async def admin_user(async_session_test):
    async with async_session_test() as db:
        # Создаем нового пользователя
        new_user = Users(
            first_name=None,
            last_name=None,
            father_name=None,
            full_name=None,
            position=None,
            phone=None,
            email=None,
            telegram=None,
            birthday=None,
            category=None,
            specialization=None,
            username="admin_user",
            password=pwd_context.hash(
                "123456789"
            ),  # Обязательно хэшируйте пароли в реальном коде!
            notes=None,
            role="admin",
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
