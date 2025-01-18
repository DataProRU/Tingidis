from web_app.schemas.contracts import ContractsModel
import pytest
from datetime import datetime
from decimal import Decimal


@pytest.fixture
async def sample_contract(async_session_test, sample_object):
    async with async_session_test() as db:
        contract = ContractsModel(
            code=sample_object.id,  # Используем id созданного объекта
            name="new_test_name",
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
async def another_contract(async_session_test, another_object):
    async with async_session_test() as db:
        contract = ContractsModel(
            code=another_object.id,  # Используем id созданного объекта
            name="test_name",
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
