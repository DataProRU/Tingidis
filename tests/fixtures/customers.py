import pytest

from web_app.models.customers import CustomerModel


@pytest.fixture
async def sample_customer(async_session_test):
    async with async_session_test() as db:
        customer = CustomerModel(name="Ivan", addres="test addres", inn="test inn")
        db.add(customer)
        await db.commit()
        await db.refresh(customer)
        return customer


@pytest.fixture
async def another_customer(async_session_test):
    async with async_session_test() as db:
        customer = CustomerModel(
            name="Alex", addres="another test addres", inn="new test inn"
        )
        db.add(customer)
        await db.commit()
        await db.refresh(customer)
        return customer
