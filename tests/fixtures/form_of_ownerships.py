import pytest
from web_app.models.form_of_ownerships import FormOfOwnerships


@pytest.fixture
async def create_form(async_session_test):
    """
    Универсальная фикстура для создания форм собственности с заданными параметрами.
    """

    async def _create_form(name: str):
        async with async_session_test() as db:
            form = FormOfOwnerships(name=name)
            db.add(form)
            await db.commit()
            await db.refresh(form)
            return form

    return _create_form


@pytest.fixture
async def sample_form(create_form):
    """
    Фикстура для создания тестовой формы собственности.
    """
    return await create_form(name="test name")


@pytest.fixture
async def another_form(create_form):
    """
    Фикстура для создания другой тестовой формы собственности.
    """
    return await create_form(name="test name 2")


@pytest.fixture
async def third_form(create_form):
    """
    Фикстура для создания третьей формы собственности (ИП).
    """
    return await create_form(name="ИП")


@pytest.fixture
async def foth_form(create_form):
    """
    Фикстура для создания четвертой формы собственности (ЗАО).
    """
    return await create_form(name="ЗАО")


@pytest.fixture
async def fifth_form(create_form):
    """
    Фикстура для создания пятой формы собственности (ОАО).
    """
    return await create_form(name="ОАО")


@pytest.fixture
async def sixth_form(create_form):
    """
    Фикстура для создания шестой формы собственности (ПАО).
    """
    return await create_form(name="ПАО")


@pytest.fixture
async def seventh_form(create_form):
    """
    Фикстура для создания седьмой формы собственности (НКО).
    """
    return await create_form(name="НКО")


@pytest.fixture
async def eighth_form(create_form):
    """
    Фикстура для создания восьмой формы собственности (Фонд).
    """
    return await create_form(name="Фонд")
