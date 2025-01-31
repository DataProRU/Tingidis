from web_app.models.contracts import Contracts
import pytest
from datetime import datetime
from decimal import Decimal


@pytest.fixture
async def sample_contract(
    async_session_test, sample_object, sample_customer, sample_user
):
    async with async_session_test() as db:
        contract = Contracts(
            code=sample_object.id,
            name="new_test_name",
            customer=sample_customer.id,
            executor=sample_user.id,
            number="123456",
            sign_date=datetime(2024, 1, 1),
            price=Decimal("2000.21"),
            theme="test_theme",
            evolution="test evolution",
        )
        db.add(contract)
        await db.commit()
        await db.refresh(contract)
        return contract


@pytest.fixture
async def another_contract(
    async_session_test, another_object, another_customer, another_user
):
    async with async_session_test() as db:
        contract = Contracts(
            code=another_object.id,  # Используем id созданного объекта
            name="test_name",
            customer=another_customer.id,
            executor=another_user.id,
            number="654321",
            sign_date=datetime(2024, 2, 2),
            price=Decimal("100.21"),
            theme="test_theme",
            evolution="test evolution",
        )
        db.add(contract)
        await db.commit()
        await db.refresh(contract)
        return contract
