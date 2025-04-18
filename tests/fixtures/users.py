from datetime import date
import pytest
from web_app.models.users import Users
from web_app.routes.auth import pwd_context


@pytest.fixture
async def create_user(async_session_test):
    """
    Универсальная фикстура для создания пользователей с заданными параметрами.
    """

    async def _create_user(
        first_name: str,
        last_name: str,
        father_name: str,
        full_name: str,
        position=None,
        phone=None,
        email=None,
        telegram=None,
        birthday=None,
        category=None,
        specialization=None,
        username: str = "user",
        password: str = "123456789",  # По умолчанию пароль, который будет хэшироваться
        notes=None,
        role="user",
        notification=None
    ):
        async with async_session_test() as db:
            user = Users(
                first_name=first_name,
                last_name=last_name,
                father_name=father_name,
                full_name=full_name,
                position=position,
                phone=phone,
                email=email,
                telegram=telegram,
                birthday=birthday,
                category=category,
                specialization=specialization,
                username=username,
                password=pwd_context.hash(password),  # Хэшируем пароль
                notes=notes,
                role=role,
                notification=notification
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user

    return _create_user


@pytest.fixture
async def sample_user(create_user):
    """
    Фикстура для создания тестового пользователя.
    """
    return await create_user(
        first_name="Ivan",
        last_name="Ivanov",
        father_name="Ivanovich",
        full_name="Ivan Ivanovich",
        username="user 1",
        password="123456789",
        position="painter",
        phone="+7(911) 337 65 43",
        email="ivan@example.com",
        telegram="@ivan_paint",
        birthday=date(1981, 12, 30),
        category="paint",
        specialization="Painter house",
        notes="sample test user",
        notification=True
    )


@pytest.fixture
async def another_user(create_user):
    """
    Фикстура для создания другого тестового пользователя.
    """
    return await create_user(
        first_name="Alex",
        last_name="Alexeev",
        father_name="Alekseevich",
        full_name="Alex Ivanovich",
        position="Worker",
        phone="+3 (911) 181 00 32",
        email="alex@mail.com",
        telegram="@alex",
        birthday=date(2001, 2, 2),
        category="test user",
        specialization="Working",
        username="user_alex",
        password="123456789qqFF_",
        notes="another test user",
        notification=True
    )


@pytest.fixture
async def admin_user(create_user):
    """
    Фикстура для создания пользователя с ролью администратора.
    """
    return await create_user(
        first_name="Vasya",
        last_name="Pupkin",
        father_name="Vasilyevich",
        full_name="Vasya Pupkin",
        username="admin_user",
        password="123456789",
        role="admin",
        notes="another test user",
    )


@pytest.fixture
async def third_user(create_user):
    """
    Фикстура для создания третьего тестового пользователя.
    """
    return await create_user(
        first_name="Maria",
        last_name="Sidorova",
        father_name="Petrovna",
        full_name="Maria Petrovna Sidorova",
        position="Manager",
        phone="+7 (921) 123 45 67",
        email="maria@example.com",
        telegram="@maria",
        birthday=date(1995, 5, 15),
        category="manager",
        specialization="Project Management",
        username="user_maria",
        password="securepassword123",
        notes="Third test user",
    )


@pytest.fixture
async def fourth_user(create_user):
    """
    Фикстура для создания четвертого тестового пользователя.
    """
    return await create_user(
        first_name="Petr",
        last_name="Smirnov",
        father_name="Nikolaevich",
        full_name="Petr Nikolaevich Smirnov",
        position="Developer",
        phone="+7 (911) 987 65 43",
        email="petr@example.com",
        telegram="@petr_developer",
        birthday=date(1985, 11, 30),
        category="developer",
        specialization="Backend Development",
        username="user_petr 4",
        password="developerpass2023",
        notes="Fourth test user",
    )
