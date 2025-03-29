import pytest

from web_app.models.customers import Customers


@pytest.fixture
async def sample_customer(async_session_test, sample_form):
    async with async_session_test() as db:
        customer = Customers(
            name="Ivan",
            form=sample_form.id,
            address="test addres",
            inn="test inn",
            notes=None,
        )
        db.add(customer)
        await db.commit()
        await db.refresh(customer)
        return customer


@pytest.fixture
async def another_customer(async_session_test, another_form):
    async with async_session_test() as db:
        customer = Customers(
            name="Alex",
            form=another_form.id,
            address="another test addres",
            inn="new test inn",
            notes="Test notes",
        )
        db.add(customer)
        await db.commit()
        await db.refresh(customer)
        return customer


@pytest.fixture
async def third_customer(async_session_test, third_form):
    async with async_session_test() as db:
        customer = Customers(
            name="Nicolas",
            form=third_form.id,
            address="second",
            inn="111111",
            notes="aaa",
        )
        db.add(customer)
        await db.commit()
        await db.refresh(customer)
        return customer


@pytest.fixture
async def fouth_customer(async_session_test, foth_form):
    async with async_session_test() as db:
        customer = Customers(
            name="John",
            form=foth_form.id,
            address="second",
            inn="22222",
            notes="bbbbb",
        )
        db.add(customer)
        await db.commit()
        await db.refresh(customer)
        return customer
