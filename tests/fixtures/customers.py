import pytest

from web_app.models.customers import Customers


@pytest.fixture
async def sample_customer(async_session_test):
    async with async_session_test() as db:
        customer = Customers(name="Ivan", address="test addres", inn="test inn")
        db.add(customer)
        await db.commit()
        await db.refresh(customer)
        return customer


@pytest.fixture
async def another_customer(async_session_test):
    async with async_session_test() as db:
        customer = Customers(
            name="Alex", address="another test addres", inn="new test inn"
        )
        db.add(customer)
        await db.commit()
        await db.refresh(customer)
        return customer
