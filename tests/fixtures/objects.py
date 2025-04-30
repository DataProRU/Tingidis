import pytest
from web_app.models.objects import Objects


@pytest.fixture
async def create_object(async_session_test):
    """
    Универсальная фикстура для создания объектов с заданными параметрами.
    """

    async def _create_object(code: str, name: str, comment: str = None):
        async with async_session_test() as db:
            obj = Objects(code=code, name=name, comment=comment)
            db.add(obj)
            await db.commit()
            await db.refresh(obj)
            return obj

    return _create_object


@pytest.fixture
async def sample_object(create_object):
    return await create_object(code="123456", name="test name", comment="OBJ 1 notes")


@pytest.fixture
async def another_object(create_object):
    return await create_object(
        code="123457", name="test name 2", comment="test comment 2"
    )


@pytest.fixture
async def second_object(create_object):
    return await create_object(
        code="234567", name="second object", comment="second object comment"
    )


@pytest.fixture
async def third_object(create_object):
    return await create_object(
        code="345678", name="third object", comment="third object comment"
    )
