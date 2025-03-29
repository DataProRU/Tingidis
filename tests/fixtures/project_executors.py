import pytest
from web_app.models.project_executors import ProjectExecutors


@pytest.fixture
async def create_project_executor(async_session_test):
    """
    Универсальная фикстура для создания исполнителей проектов с заданными параметрами.
    """

    async def _create_project_executor(user_id, project_id):
        async with async_session_test() as db:
            project_executor = ProjectExecutors(user=user_id, project=project_id)
            db.add(project_executor)
            await db.commit()
            await db.refresh(project_executor)
            return project_executor

    return _create_project_executor


@pytest.fixture
async def sample_project_executor(create_project_executor, sample_user, sample_project):
    """
    Фикстура для создания тестового исполнителя проекта.
    """
    return await create_project_executor(
        user_id=sample_user.id, project_id=sample_project.id
    )


@pytest.fixture
async def another_project_executor(
    create_project_executor, another_user, another_project
):
    """
    Фикстура для создания другого тестового исполнителя проекта.
    """
    return await create_project_executor(
        user_id=another_user.id, project_id=another_project.id
    )


@pytest.fixture
async def third_project_executor(create_project_executor, third_user, third_project):
    """
    Фикстура для создания третьего тестового исполнителя проекта.
    """
    return await create_project_executor(
        user_id=third_user.id, project_id=third_project.id
    )


@pytest.fixture
async def on_hold_project_executor(
    create_project_executor, fourth_user, on_hold_project
):
    """
    Фикстура для создания исполнителя проекта со статусом "On Hold".
    """
    return await create_project_executor(
        user_id=fourth_user.id, project_id=on_hold_project.id
    )
