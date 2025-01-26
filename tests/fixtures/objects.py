import pytest

from web_app.models.objects import Objects


@pytest.fixture
async def sample_object(async_session_test):
    async with async_session_test() as db:
        object = Objects(code="123456", name="test name", comment=None)
        db.add(object)
        await db.commit()
        await db.refresh(object)
        return object


@pytest.fixture
async def another_object(async_session_test):
    async with async_session_test() as db:
        object = Objects(code="123457", name="test name 2", comment="test comment 2")
        db.add(object)
        await db.commit()
        await db.refresh(object)
        return object
