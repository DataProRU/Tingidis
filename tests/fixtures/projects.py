import pytest
from datetime import date
from web_app.models.projects import Projects


@pytest.fixture
async def create_project(async_session_test):
    """
    Универсальная фикстура для создания проектов с заданными параметрами.
    """

    async def _create_project(
        object_id,
        contract_id=None,
        name="test project",
        number="12345",
        main_executor_id=None,
        deadline=date(2024, 1, 1),
        status_id=None,
        notes=None,
    ):
        async with async_session_test() as db:
            project = Projects(
                object=object_id,
                contract=contract_id,
                name=name,
                number=number,
                main_executor=main_executor_id,
                deadline=deadline,
                status=status_id,
                notes=notes,
            )
            db.add(project)
            await db.commit()
            await db.refresh(project)
            return project

    return _create_project


@pytest.fixture
async def sample_project(
    create_project, sample_object, sample_contract, sample_user, sample_project_status
):
    """
    Фикстура для создания тестового проекта.
    """
    return await create_project(
        object_id=sample_object.id,
        contract_id=sample_contract.id,
        name="test project 1",
        number="11111",
        main_executor_id=sample_user.id,
        deadline=date(2024, 2, 1),
        status_id=sample_project_status.id,
        notes="sample notes",
    )


@pytest.fixture
async def another_project(
    create_project,
    another_object,
    another_user,
    another_project_status,
    another_contract,
):
    """
    Фикстура для создания другого тестового проекта.
    """
    return await create_project(
        object_id=another_object.id,
        contract_id=another_contract.id,
        name="test project 2",
        number="222",
        main_executor_id=another_user.id,
        deadline=date(2024, 2, 4),
        status_id=another_project_status.id,
        notes="another notes",
    )


@pytest.fixture
async def third_project(
    create_project, third_object, third_contract, third_user, completed_status
):
    """
    Фикстура для создания третьего тестового проекта.
    """
    return await create_project(
        object_id=third_object.id,
        contract_id=third_contract.id,
        name="Completed Project",
        number="333",
        main_executor_id=third_user.id,
        deadline=date(2023, 12, 31),
        status_id=completed_status.id,
        notes="This project is completed.",
    )


@pytest.fixture
async def on_hold_project(
    create_project, fourth_object, fourth_user, on_hold_project_status
):
    """
    Фикстура для создания проекта со статусом "On Hold".
    """
    return await create_project(
        object_id=fourth_object.id,
        contract_id=None,
        name="On Hold Project",
        number="444",
        main_executor_id=fourth_user.id,
        deadline=date(2024, 6, 1),
        status_id=on_hold_project_status.id,
        notes="This project is currently on hold.",
    )
