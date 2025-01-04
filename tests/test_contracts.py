"""import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.future import select
from datetime import date
from web_app.database import Base, Contract  # Импорт моделей и базы данных
from web_app.services.contracts_services import (
    get_all_contracts,
    get_contract_by_id,
    edit_contract,
    add_new_contract,
    service_delete_contract,
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


# Тест на добавление нового контракта
@pytest.mark.asyncio
async def test_add_new_contract(db: AsyncSession):
    await add_new_contract(
        contract_code=1,
        object_name="Test Object",
        customer="Customer A",
        executer="Executor A",
        contract_number="12345",
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
    assert result[0].contract_code == 1
    assert result[0].object_name == "Test Object"
    assert result[0].customer == "Customer A"
    assert result[0].executer == "Executor A"
    assert result[0].contract_number == "12345"
    assert result[0].status == "New"
    assert result[0].stage == "Start"
    assert result[0].contract_scan == "scan_1.pdf"
    assert result[0].original_scan == "original_1.pdf"
    assert result[0].percent_complite == 0
    assert result[0].date_start == date(2024, 1, 1)
    assert result[0].date_finish == date(2024, 12, 31)
    assert result[0].cost == 100000
    assert result[0].money_received == 50000
    assert result[0].scan_complited_act == "completed_scan.pdf"
    assert result[0].original_complited_act == "completed_original.pdf"
    assert result[0].volumes == "Volume 1"
    assert result[0].notes == "Initial Test Contract"


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
async def test_update_contract_code(db: AsyncSession):
    await test_add_new_contract(db)  # Добавляем тестовые данные
    await edit_contract(
        contract_id=1,
        db=db,
        contract_code=2,
        object_name="Updated Object",
        customer="Updated Customer",
        executer="Updated Executor",
        contract_number="54321",
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
    assert updated_contract.contract_code == 2


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "field, new_value, expected_value",
    [
        ("contract_code", 2, 2),
        ("object_name", "Updated Object", "Updated Object"),
        ("customer", "Updated Customer", "Updated Customer"),
        ("executer", "Updated Executor", "Updated Executor"),
        ("contract_number", "54321", "54321"),
        ("status", "Updated", "Updated"),
        ("stage", "End", "End"),
        ("contract_scan", "updated_scan.pdf", "updated_scan.pdf"),
        ("original_scan", "updated_original.pdf", "updated_original.pdf"),
        ("percent_complite", 100, 100),
        ("date_start", date(2024, 1, 1), date(2024, 1, 1)),
        ("date_finish", date(2024, 12, 31), date(2024, 12, 31)),
        ("cost", 200000, 200000),
        ("money_received", 200000, 200000),
        ("money_left", 0, 0),
        (
            "scan_complited_act",
            "updated_scan_completed.pdf",
            "updated_scan_completed.pdf",
        ),
        (
            "original_complited_act",
            "updated_original_completed.pdf",
            "updated_original_completed.pdf",
        ),
        ("volumes", "Volume Updated", "Volume Updated"),
        ("notes", "Updated Contract", "Updated Contract"),
    ],
)
async def test_update_contract_field(
    db: AsyncSession, field, new_value, expected_value
):
    await test_add_new_contract(db)  # Добавляем тестовые данные

    # Получаем текущие данные контракта
    current_contract = await get_contract_by_id(1, db)

    # Обновляем только одно поле
    update_data = {
        "contract_code": current_contract.contract_code,
        "object_name": current_contract.object_name,
        "customer": current_contract.customer,
        "executer": current_contract.executer,
        "contract_number": current_contract.contract_number,
        "status": current_contract.status,
        "stage": current_contract.stage,
        "contract_scan": current_contract.contract_scan,
        "original_scan": current_contract.original_scan,
        "percent_complite": current_contract.percent_complite,
        "date_start": current_contract.date_start,
        "date_finish": current_contract.date_finish,
        "cost": current_contract.cost,
        "money_received": current_contract.money_received,
        "money_left": current_contract.money_left,
        "scan_complited_act": current_contract.scan_complited_act,
        "original_complited_act": current_contract.original_complited_act,
        "volumes": current_contract.volumes,
        "notes": current_contract.notes,
    }
    update_data[field] = new_value

    await update_contract(contract_id=1, db=db, **update_data)

    # Получаем обновленные данные контракта
    updated_contract = await get_contract_by_id(1, db)

    # Проверяем, что обновленное поле имеет ожидаемое значение
    assert getattr(updated_contract, field) == expected_value

    # Проверяем, что остальные поля остались неизменными
    for key, value in update_data.items():
        if key != field:
            assert getattr(updated_contract, key) == getattr(current_contract, key)


@pytest.mark.asyncio
async def test_update_customer(db: AsyncSession):
    await test_add_new_contract(db)  # Добавляем тестовые данные
    await update_contract(
        contract_id=1,
        db=db,
        contract_code=1,
        object_name="Object",
        customer="Updated Customer",
        executer="Executor",
        contract_number="12345",
        status="Status",
        stage="Stage",
        contract_scan="scan.pdf",
        original_scan="original.pdf",
        percent_complite=50,
        date_start=date(2023, 1, 1),
        date_finish=date(2023, 12, 31),
        cost=100000,
        money_received=50000,
        money_left=50000,
        scan_complited_act="scan_completed.pdf",
        original_complited_act="original_completed.pdf",
        volumes="Volumes",
        notes="Notes",
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
"""
