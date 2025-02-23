import pytest
from datetime import date
from web_app.models.projects import Projects


@pytest.fixture
async def sample_project(
    async_session_test,
    sample_object,
    sample_contract,
    sample_user,
    sample_project_status,
):
    async with async_session_test() as db:
        project = Projects(
            object=sample_object.id,
            contract=sample_contract.id,
            name="test contract",
            number="11111",
            main_executor=sample_user.id,
            deadline=date(2001, 2, 2),
            status=sample_project_status.id,
            notes="sample notes",
        )
        db.add(project)
        await db.commit()
        await db.refresh(project)
        return project


@pytest.fixture
async def another_project(
    async_session_test,
    another_object,
    another_contract,
    another_user,
    another_project_status,
):
    async with async_session_test() as db:
        project = Projects(
            object=another_object.id,
            contract=None,
            name="test contract",
            number="222",
            main_executor=another_user.id,
            deadline=date(2001, 2, 2),
            status=another_project_status.id,
            notes=None,
        )
        db.add(project)
        await db.commit()
        await db.refresh(project)
        return project
