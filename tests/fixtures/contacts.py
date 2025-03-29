import pytest
from web_app.models.contacts import Contacts


@pytest.fixture
async def create_contact(async_session_test):
    """
    Универсальная фикстура для создания контактов с заданными параметрами.
    """

    async def _create_contact(
        first_name,
        last_name,
        father_name=None,
        email=None,
        phone=None,
        position=None,
        customer_id=None,
    ):
        async with async_session_test() as db:
            contact = Contacts(
                first_name=first_name,
                last_name=last_name,
                father_name=father_name,
                email=email,
                phone=phone,
                position=position,
                customer=customer_id,
            )
            db.add(contact)
            await db.commit()
            await db.refresh(contact)
            return contact

    return _create_contact


@pytest.fixture
async def sample_contact(create_contact, sample_customer):
    """
    Фикстура для создания тестового контакта.
    """
    return await create_contact(
        first_name="Ivan",
        last_name="Ivanov",
        father_name="Ivanovich",
        email="ivanov@mail.com",
        phone="+70000000000",
        position="worker",
        customer_id=sample_customer.id,
    )


@pytest.fixture
async def another_contact(create_contact, another_customer):
    """
    Фикстура для создания другого тестового контакта.
    """
    return await create_contact(
        first_name="Alex",
        last_name="Alexeev",
        father_name="Alexeevich",
        email="aled@mail.com",
        phone="+70000000001",
        position="engineer",
        customer_id=another_customer.id,
    )


@pytest.fixture
async def third_contact(create_contact, third_customer):
    """
    Фикстура для создания третьего тестового контакта.
    """
    return await create_contact(
        first_name="Maria",
        last_name="Sidorova",
        father_name="Petrovna",
        email="maria@example.com",
        phone="+79112345678",
        position="manager",
        customer_id=third_customer.id,
    )


@pytest.fixture
async def fourth_contact(create_contact, fouth_customer):
    """
    Фикстура для создания четвертого тестового контакта.
    """
    return await create_contact(
        first_name="Petr",
        last_name="Smirnov",
        father_name="Nikolaevich",
        email="petr@example.com",
        phone="+79118765432",
        position="developer",
        customer_id=fouth_customer.id,
    )
