import pytest

from web_app.models.project_executors import ProjectExecutors


@pytest.fixture
async def sample_project_executor(async_session_test, sample_user, sample_project):
    async with async_session_test() as db:
        project_executor = ProjectExecutors(
            user=sample_user.id, project=sample_project.id
        )
        db.add(project_executor)
        await db.commit()
        await db.refresh(project_executor)
        return project_executor


@pytest.fixture
async def another_project_executor(async_session_test, another_user, another_project):
    async with async_session_test() as db:
        project_executor = ProjectExecutors(
            user=another_user.id, project=another_project.id
        )
        db.add(project_executor)
        await db.commit()
        await db.refresh(project_executor)
        return object
