import pytest

from web_app.models.person_contacts import PersonContracts


@pytest.fixture
async def sample_person_contract(async_session_test, sample_customer):
    async with async_session_test() as db:
        person_contract = PersonContracts(
            first_name="Ivan",
            last_name="Ivanov",
            father_name="Ivanovich",
            email="ivanov@mail.com",
            position="worker",
            customer=sample_customer.id,
        )
        db.add(person_contract)
        await db.commit()
        await db.refresh(person_contract)
        return person_contract


@pytest.fixture
async def another_person_contract(async_session_test, another_customer):
    async with async_session_test() as db:
        person_contract = PersonContracts(
            first_name="Alex",
            last_name="Alexeev",
            father_name="Alexeevich",
            email="aled@mail.com",
            position="engineer",
            customer=another_customer.id,
        )
        db.add(person_contract)
        await db.commit()
        await db.refresh(person_contract)
        return person_contract
