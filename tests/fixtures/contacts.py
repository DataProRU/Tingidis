import pytest

from web_app.models.contacts import Contacts


@pytest.fixture
async def sample_contact(async_session_test, sample_customer):
    async with async_session_test() as db:
        contact = Contacts(
            first_name="Ivan",
            last_name="Ivanov",
            father_name="Ivanovich",
            email="ivanov@mail.com",
            phone="+70000000000",
            position="worker",
            customer=sample_customer.id,
        )
        db.add(contact)
        await db.commit()
        await db.refresh(contact)
        return contact


@pytest.fixture
async def another_contact(async_session_test, another_customer):
    async with async_session_test() as db:
        contact = Contacts(
            first_name="Alex",
            last_name="Alexeev",
            father_name="Alexeevich",
            phone="+70000000001",
            email="aled@mail.com",
            position="engineer",
            customer=another_customer.id,
        )
        db.add(contact)
        await db.commit()
        await db.refresh(contact)
        return contact
