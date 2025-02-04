import pytest

from web_app.models.form_of_ownerships import FormOfOwnerships


@pytest.fixture
async def sample_form(async_session_test):
    async with async_session_test() as db:
        form = FormOfOwnerships(name="test name")
        db.add(form)
        await db.commit()
        await db.refresh(form)
        return form


@pytest.fixture
async def another_form(async_session_test):
    async with async_session_test() as db:
        form = FormOfOwnerships(name="test name 2")
        db.add(form)
        await db.commit()
        await db.refresh(form)
        return form
