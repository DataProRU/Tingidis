import pytest
from web_app.models.project_statuses import ProjectStatuses


@pytest.fixture
async def create_project_status(async_session_test):
    """
    Универсальная фикстура для создания статусов проектов с заданными параметрами.
    """

    async def _create_project_status(name: str):
        async with async_session_test() as db:
            project_status = ProjectStatuses(name=name)
            db.add(project_status)
            await db.commit()
            await db.refresh(project_status)
            return project_status

    return _create_project_status


@pytest.fixture
async def sample_project_status(create_project_status):
    """
    Фикстура для создания тестового статуса проекта.
    """
    return await create_project_status(name="sample status")


@pytest.fixture
async def another_project_status(create_project_status):
    """
    Фикстура для создания другого тестового статуса проекта.
    """
    return await create_project_status(name="another status")


@pytest.fixture
async def in_progress_status(create_project_status):
    """
    Фикстура для создания статуса "In Progress".
    """
    return await create_project_status(name="In Progress")


@pytest.fixture
async def completed_status(create_project_status):
    """
    Фикстура для создания статуса "Completed".
    """
    return await create_project_status(name="Completed")


@pytest.fixture
async def on_hold_status(create_project_status):
    """
    Фикстура для создания статуса "On Hold".
    """
    return await create_project_status(name="On Hold")


@pytest.fixture
async def canceled_status(create_project_status):
    """
    Фикстура для создания статуса "Canceled".
    """
    return await create_project_status(name="Canceled")
