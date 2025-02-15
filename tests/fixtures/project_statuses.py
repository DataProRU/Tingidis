import pytest

from web_app.models.project_statuses import ProjectStatuses


@pytest.fixture
async def sample_project_status(async_session_test):
    async with async_session_test() as db:
        form = ProjectStatuses(name="test project name")
        db.add(form)
        await db.commit()
        await db.refresh(form)
        return form


@pytest.fixture
async def another_project_status(async_session_test):
    async with async_session_test() as db:
        form = ProjectStatuses(name="test project name")
        db.add(form)
        await db.commit()
        await db.refresh(form)
        return form
