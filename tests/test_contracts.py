import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.future import select
from datetime import date
from web_app.database import Base, Contract  # Импорт моделей и базы данных
from web_app.services.contracts_services import (
    get_all_contracts,
    get_contract_by_id,
    update_contract,
    add_new_contract,
    service_delete_contract,
)

# Фикстура для создания асинхронного движка
@pytest.fixture
async def async_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")  # In-memory база данных
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

# Тест на добавление нового контракта
@pytest.mark.asyncio
async def test_add_new_contract(db: AsyncSession):
    await add_new_contract(
        contract_code=1,
        object_name="Test Object",
        customer="Customer A",
        executer="Executor A",
        contract_number=12345,
        status="New",
        stage="Start",
        contract_scan="scan_1.pdf",
        original_scan="original_1.pdf",
        percent_complite=0,
        date_start=date(2024, 1, 1),
        date_finish=date(2024, 12, 31),
        cost=100000,
        money_received=50000,
        money_left=50000,
        scan_complited_act="completed_scan.pdf",
        original_complited_act="completed_original.pdf",
        volumes="Volume 1",
        notes="Initial Test Contract",
        db=db,
    )
    stmt = await db.execute(select(Contract))
    result = stmt.scalars().all()
    assert len(result) == 1
    assert result[0].customer == "Customer A"

# Тест на получение всех контрактов
@pytest.mark.asyncio
async def test_get_all_contracts(db: AsyncSession):
    await test_add_new_contract(db)  # Добавляем тестовые данные
    contracts = await get_all_contracts(db)
    assert len(contracts) == 1
    assert contracts[0].customer == "Customer A"

# Тест на получение контракта по ID
@pytest.mark.asyncio
async def test_get_contract_by_id(db: AsyncSession):
    await test_add_new_contract(db)  # Добавляем тестовые данные
    contract = await get_contract_by_id(1, db)
    assert contract is not None
    assert contract.contract_code == 1

# Тест на обновление контракта
@pytest.mark.asyncio
async def test_update_contract(db: AsyncSession):
    await test_add_new_contract(db)  # Добавляем тестовые данные
    await update_contract(
        contract_id=1,
        db=db,
        contract_code=1,
        object_name="Updated Object",
        customer="Updated Customer",
        executer="Updated Executor",
        contract_number=54321,
        status="Updated",
        stage="End",
        contract_scan="updated_scan.pdf",
        original_scan="updated_original.pdf",
        percent_complite=100,
        date_start=date(2024, 1, 1),
        date_finish=date(2024, 12, 31),
        cost=200000,
        money_received=200000,
        money_left=0,
        scan_complited_act="updated_scan_completed.pdf",
        original_complited_act="updated_original_completed.pdf",
        volumes="Volume Updated",
        notes="Updated Contract",
    )
    updated_contract = await get_contract_by_id(1, db)
    assert updated_contract.customer == "Updated Customer"

# Тест на удаление контракта
@pytest.mark.asyncio
async def test_service_delete_contract(db: AsyncSession):
    await test_add_new_contract(db)  # Добавляем тестовые данные
    await service_delete_contract(1, db)
    stmt = await db.execute(select(Contract))
    result = stmt.scalars().all()
    assert len(result) == 0
