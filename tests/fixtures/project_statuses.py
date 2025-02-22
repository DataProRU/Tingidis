import pytest

from web_app.models.project_statuses import ProjectStatuses


@pytest.fixture
async def sample_project_status(async_session_test):
    async with async_session_test() as db:
        project_status = ProjectStatuses(name="sample status")
        db.add(project_status)
        await db.commit()
        await db.refresh(project_status)
        return project_status


@pytest.fixture
async def another_project_status(async_session_test):
    async with async_session_test() as db:
        project_status = ProjectStatuses(name="another status")
        db.add(project_status)
        await db.commit()
        await db.refresh(project_status)
        return project_status
