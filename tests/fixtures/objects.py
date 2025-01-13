from datetime import date

import pytest

from web_app.schemas.objects import ObjectModel


@pytest.fixture
async def sample_object(async_session_test):
    async with async_session_test() as db:
        object = ObjectModel(code="123456", name="test name", comment="test comment")
        db.add(object)
        await db.commit()
        await db.refresh(object)
        return object


@pytest.fixture
async def another_object(async_session_test):
    async with async_session_test() as db:
        object = ObjectModel(
            code="123457", name="test name 2", comment="test comment 2"
        )
        db.add(object)
        await db.commit()
        await db.refresh(object)
        return object
