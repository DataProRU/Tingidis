import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.future import select
from datetime import date
from web_app.database import Base, WebUser  # Импорт моделей и базы данных
from web_app.services.users_services import (
    get_all_users,
    get_user_by_id,
    update_user_service,
    add_new_user,
    delete_user_service,
)


# Фикстура для создания асинхронного движка
@pytest.fixture
async def async_engine():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:"
    )  # In-memory база данных
    yield engine
    await engine.dispose()


# Фикстура для фабрики сессий
@pytest.fixture
async def session_factory(async_engine):
    return async_sessionmaker(bind=async_engine, expire_on_commit=False)


# Фикстура для подключения к базе данных
@pytest.fixture
async def db(session_factory) -> AsyncSession:
    async with session_factory() as session:
        yield session


# Фикстура для инициализации базы данных (создает и удаляет таблицы для каждого теста)
@pytest.fixture(autouse=True)
async def init_db(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Тест на добавление нового пользователя
@pytest.mark.asyncio
async def test_add_new_contract(db: AsyncSession):
    await add_new_user(
        last_name="Ivan",
        first_name="Ivanov",
        middle_name="Ivanovich",
        position="Enginer",
        phone="+7 (911) 481 00 52",
        email="ivanov@mail.com",
        telegram="@ivan",
        birthdate=date(2024, 1, 1),
        category="test user",
        specialization="Enginiring",
        notes="test user",
        login="user",
        password="123456789",
        role="user",
        db=db,
    )
    stmt = await db.execute(select(WebUser))
    result = stmt.scalars().all()
    assert len(result) == 1
    assert result[0].email == "ivanov@mail.com"


# Тест на получение всех контрактов
@pytest.mark.asyncio
async def test_get_all_contracts(db: AsyncSession):
    await test_add_new_contract(db)  # Добавляем тестовые данные
    contracts = await get_all_users(db)
    assert len(contracts) == 1
    assert contracts[0].last_name == "Ivan"


# Тест на получение контракта по ID
@pytest.mark.asyncio
async def test_get_contract_by_id(db: AsyncSession):
    await test_add_new_contract(db)  # Добавляем тестовые данные
    user = await get_user_by_id(1, db)
    assert user is not None
    assert user.last_name == "Ivan"


# Тест на обновление контракта
@pytest.mark.asyncio
async def test_update_contract(db: AsyncSession):
    await test_add_new_contract(db)  # Добавляем тестовые данные
    await update_user_service(
        user_id=1,
        db=db,
        role="admin",
        last_name="Ivan",
        first_name="Updated User",
        middle_name="Updated Executor",
        position="Test",
        phone="+7 (911) 481 00 52",
        email="ivanov@mail.com",
        telegram="@ivan",
        birthdate=date(2024, 1, 1),
        category="test user",
        specialization="Enginiring",
        notes="test user",
    )
    updated_user = await get_user_by_id(1, db)
    assert updated_user.first_name == "Updated User"


# Тест на удаление пользователя
@pytest.mark.asyncio
async def test_service_delete_contract(db: AsyncSession):
    await test_add_new_contract(db)  # Добавляем тестовые данные
    await delete_user_service(1, db)
    stmt = await db.execute(select(WebUser))
    result = stmt.scalars().all()
    assert len(result) == 0
