import pytest


@pytest.mark.asyncio
async def test_sort_project_executors_by_user_full_name_asc(
    client, sample_project_executor, another_project_executor, third_project_executor
):
    """
    Тест сортировки исполнителей проектов по полному имени пользователя в порядке возрастания.
    """
    response = client.get(
        "/project-executors", params={"sortBy": "user_full_name", "sortDir": "asc"}
    )
    assert response.status_code == 200

    executors = response.json()
    assert len(executors) >= 3
    assert executors[0]["user"]["full_name"] == "Alex Ivanovich"
    assert executors[1]["user"]["full_name"] == "Ivan Ivanovich"
    assert executors[2]["user"]["full_name"] == "Maria Petrovna Sidorova"


@pytest.mark.asyncio
async def test_sort_project_executors_by_user_full_name_desc(
    client, sample_project_executor, another_project_executor, third_project_executor
):
    """
    Тест сортировки исполнителей проектов по полному имени пользователя в порядке убывания.
    """
    response = client.get(
        "/project-executors",
        params={"sortBy": "user_full_name", "sortDir": "desc"},
    )
    assert response.status_code == 200

    executors = response.json()
    assert len(executors) >= 3
    assert executors[0]["user"]["full_name"] == "Maria Petrovna Sidorova"
    assert executors[1]["user"]["full_name"] == "Ivan Ivanovich"
    assert executors[2]["user"]["full_name"] == "Alex Ivanovich"


@pytest.mark.asyncio
async def test_sort_project_executors_by_project_name_asc(
    client, sample_project_executor, another_project_executor, third_project_executor
):
    """
    Тест сортировки исполнителей проектов по имени проекта в порядке возрастания.
    """
    response = client.get(
        "/project-executors", params={"sortBy": "project_name", "sortDir": "asc"}
    )
    assert response.status_code == 200

    executors = response.json()
    assert len(executors) >= 3
    assert executors[0]["project"]["name"] == "Completed Project"
    assert executors[1]["project"]["name"] == "test project 1"
    assert executors[2]["project"]["name"] == "test project 2"


@pytest.mark.asyncio
async def test_sort_project_executors_by_project_name_desc(
    client, sample_project_executor, another_project_executor, third_project_executor
):
    """
    Тест сортировки исполнителей проектов по имени проекта в порядке убывания.
    """
    response = client.get(
        "/project-executors", params={"sortBy": "project_name", "sortDir": "desc"}
    )
    assert response.status_code == 200

    executors = response.json()
    assert len(executors) >= 3
    assert executors[0]["project"]["name"] == "test project 2"
    assert executors[1]["project"]["name"] == "test project 1"
    assert executors[2]["project"]["name"] == "Completed Project"


@pytest.mark.asyncio
async def test_sort_project_executors_by_invalid_field(client):
    """
    Тест попытки сортировки по несуществующему полю.
    """
    response = client.get(
        "/project-executors", params={"sortBy": "invalid_field", "sortDir": "asc"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Поле 'invalid_field' не найдено"
