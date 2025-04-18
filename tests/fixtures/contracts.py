import pytest
from datetime import datetime
from decimal import Decimal
from web_app.models.contracts import Contracts


@pytest.fixture
async def create_contract(async_session_test):
    """
    Универсальная фикстура для создания контрактов с заданными параметрами.
    """

    async def _create_contract(
        code,
        name,
        customer_id,
        executor_id,
        number="123456",
        sign_date=datetime(2024, 1, 1),
        price=Decimal("2000.21"),
        theme="test_theme",
        evolution=None,
    ):
        async with async_session_test() as db:
            contract = Contracts(
                code=code,
                name=name,
                customer=customer_id,
                executor=executor_id,
                number=number,
                sign_date=sign_date,
                price=price,
                theme=theme,
                evolution=evolution,
            )
            db.add(contract)
            await db.commit()
            await db.refresh(contract)
            return contract

    return _create_contract


@pytest.fixture
async def sample_contract(create_contract, sample_object, sample_customer, sample_user):
    """
    Фикстура для создания тестового контракта.
    """
    return await create_contract(
        code=sample_object.id,
        name="new_test_name_1",
        customer_id=sample_customer.id,
        executor_id=sample_user.id,
        number="123456",
        sign_date=datetime(2024, 1, 1),
        price=Decimal("2000.21"),
        theme="test_theme_1",
        evolution="1. 24.01.2025 13:00:01",
    )


@pytest.fixture
async def another_contract(
    create_contract, another_object, another_customer, another_user
):
    """
    Фикстура для создания другого тестового контракта.
    """
    return await create_contract(
        code=another_object.id,
        name="test_name_2",
        customer_id=another_customer.id,
        executor_id=another_user.id,
        number="654321",
        sign_date=datetime(2024, 2, 2),
        price=Decimal("100.21"),
        theme="test_theme_2",
        evolution="2. 24.01.2025 13:00:01",
    )


@pytest.fixture
async def third_contract(create_contract, third_object, third_customer, third_user):
    """
    Фикстура для создания третьего тестового контракта.
    """
    return await create_contract(
        code=third_object.id,
        name="third_contract_name",
        customer_id=third_customer.id,
        executor_id=third_user.id,
        number="987654",
        sign_date=datetime(2024, 3, 3),
        price=Decimal("5000.50"),
        theme="third_theme",
        evolution="Updated on 2024-03-03",
    )


@pytest.fixture
async def fourth_contract(create_contract, second_object, fouth_customer, fourth_user):
    """
    Фикстура для создания четвертого тестового контракта.
    """
    return await create_contract(
        code=second_object.id,
        name="fourth_contract_name",
        customer_id=fouth_customer.id,
        executor_id=fourth_user.id,
        number="432109",
        sign_date=datetime(2024, 4, 4),
        price=Decimal("10000.00"),
        theme="fourth_theme",
        evolution=None,
    )
