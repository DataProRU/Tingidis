from datetime import date

import pytest


@pytest.mark.asyncio
async def test_sort_projects_by_object_asc(client, sample_project, another_project):
    """
    Тест сортировки пользователей по (object) в порядке возрастания.
    """
    response = client.get("/projects", params={"sortBy": "object", "sortDir": "asc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["object"]["code"] == "123456"
    assert users[1]["object"]["code"] == "123457"


@pytest.mark.asyncio
async def test_sort_projects_by_object_desc(client, sample_project, another_project):
    """
    Тест сортировки пользователей по (object) в порядке убывания.
    """
    response = client.get("/projects", params={"sortBy": "object", "sortDir": "desc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["object"]["code"] == "123457"
    assert users[1]["object"]["code"] == "123456"


@pytest.mark.asyncio
async def test_sort_projects_by_name_asc(client, sample_project, another_project):
    """
    Тест сортировки проектов по названию (name) в порядке возрастания.
    """
    response = client.get("/projects", params={"sortBy": "name", "sortDir": "asc"})
    assert response.status_code == 200

    projects = response.json()
    assert len(projects) >= 2
    assert projects[0]["name"] == "test project 1"
    assert projects[1]["name"] == "test project 2"


@pytest.mark.asyncio
async def test_sort_projects_by_name_desc(client, sample_project, another_project):
    """
    Тест сортировки проектов по названию (name) в порядке убывания.
    """
    response = client.get("/projects", params={"sortBy": "name", "sortDir": "desc"})
    assert response.status_code == 200

    projects = response.json()
    assert len(projects) >= 2
    assert projects[0]["name"] == "test project 2"
    assert projects[1]["name"] == "test project 1"


@pytest.mark.asyncio
async def test_sort_projects_by_number_asc(
    client, sample_project, another_project, third_project
):
    """
    Тест сортировки проектов по номеру (number) в порядке возрастания.
    """
    response = client.get("/projects", params={"sortBy": "number", "sortDir": "asc"})
    assert response.status_code == 200

    projects = response.json()
    assert len(projects) >= 3
    assert projects[0]["number"] == "11111"
    assert projects[1]["number"] == "222"
    assert projects[2]["number"] == "333"


@pytest.mark.asyncio
async def test_sort_projects_by_number_desc(
    client, sample_project, another_project, third_project
):
    """
    Тест сортировки проектов по номеру (number) в порядке убывания.
    """
    response = client.get("/projects", params={"sortBy": "number", "sortDir": "desc"})
    assert response.status_code == 200

    projects = response.json()
    assert len(projects) >= 3
    assert projects[0]["number"] == "333"
    assert projects[1]["number"] == "222"
    assert projects[2]["number"] == "11111"


@pytest.mark.asyncio
async def test_sort_projects_by_deadline_asc(
    client, sample_project, another_project, third_project
):
    """
    Тест сортировки проектов по сроку (deadline) в порядке возрастания.
    """
    response = client.get("/projects", params={"sortBy": "deadline", "sortDir": "asc"})
    assert response.status_code == 200

    projects = response.json()
    assert len(projects) >= 3
    assert projects[0]["deadline"] == "2023-12-31"
    assert projects[1]["deadline"] == "2024-02-01"
    assert projects[2]["deadline"] == "2024-02-04"


@pytest.mark.asyncio
async def test_sort_projects_by_deadline_desc(
    client, sample_project, another_project, third_project
):
    """
    Тест сортировки проектов по сроку (deadline) в порядке убывания.
    """
    response = client.get("/projects", params={"sortBy": "deadline", "sortDir": "desc"})
    assert response.status_code == 200

    projects = response.json()
    assert len(projects) >= 3
    assert projects[0]["deadline"] == "2024-02-04"
    assert projects[1]["deadline"] == "2024-02-01"
    assert projects[2]["deadline"] == "2023-12-31"


@pytest.mark.asyncio
async def test_sort_projects_by_status_asc(
    client, sample_project, another_project, third_project
):
    """
    Тест сортировки проектов по статусу (status) в порядке возрастания.
    """
    response = client.get("/projects", params={"sortBy": "status", "sortDir": "asc"})
    assert response.status_code == 200

    projects = response.json()
    assert len(projects) >= 3
    assert projects[0]["status"]["name"] == "another status"
    assert projects[1]["status"]["name"] == "Completed"
    assert projects[2]["status"]["name"] == "sample status"


@pytest.mark.asyncio
async def test_sort_projects_by_status_desc(
    client, sample_project, another_project, third_project
):
    """
    Тест сортировки проектов по статусу (status) в порядке убывания.
    """
    response = client.get("/projects", params={"sortBy": "status", "sortDir": "desc"})
    assert response.status_code == 200

    projects = response.json()
    assert len(projects) >= 3
    assert projects[0]["status"]["name"] == "sample status"
    assert projects[1]["status"]["name"] == "Completed"
    assert projects[2]["status"]["name"] == "another status"


@pytest.mark.asyncio
async def test_sort_projects_by_contract_asc(
    client, sample_project, another_project, third_project
):
    """
    Тест сортировки проектов по контракту (contract) в порядке возрастания.
    """
    response = client.get("/projects", params={"sortBy": "contract", "sortDir": "asc"})
    assert response.status_code == 200

    projects = response.json()
    assert len(projects) >= 3
    assert projects[0]["contract"]["number"] == "123456"
    assert projects[1]["contract"]["number"] == "654321"
    assert projects[2]["contract"]["number"] == "987654"


@pytest.mark.asyncio
async def test_sort_projects_by_contract_desc(
    client, sample_project, another_project, third_project
):
    """
    Тест сортировки проектов по контракту (contract) в порядке убывания.
    """
    response = client.get("/projects", params={"sortBy": "contract", "sortDir": "desc"})
    assert response.status_code == 200

    projects = response.json()
    assert len(projects) >= 3
    assert projects[0]["contract"]["number"] == "987654"
    assert projects[1]["contract"]["number"] == "654321"
    assert projects[2]["contract"]["number"] == "123456"


@pytest.mark.asyncio
async def test_sort_projects_by_main_executor_asc(
    client, another_project, sample_project, third_project
):
    """
    Тест сортировки проектов по исполнителю (main_executor) в порядке возрастания.
    """
    response = client.get(
        "/projects", params={"sortBy": "main_executor", "sortDir": "asc"}
    )
    assert response.status_code == 200

    projects = response.json()
    assert len(projects) >= 3
    assert projects[0]["main_executor"]["full_name"] == "Alex Ivanovich"
    assert projects[1]["main_executor"]["full_name"] == "Ivan Ivanovich"
    assert projects[2]["main_executor"]["full_name"] == "Maria Petrovna Sidorova"


@pytest.mark.asyncio
async def test_sort_projects_by_main_executor_desc(
    client, another_project, sample_project, third_project
):
    """
    Тест сортировки проектов по исполнителю (main_executor) в порядке убывания.
    """
    response = client.get(
        "/projects", params={"sortBy": "main_executor", "sortDir": "desc"}
    )
    assert response.status_code == 200

    projects = response.json()
    assert len(projects) >= 3
    assert projects[0]["main_executor"]["full_name"] == "Maria Petrovna Sidorova"
    assert projects[1]["main_executor"]["full_name"] == "Ivan Ivanovich"
    assert projects[2]["main_executor"]["full_name"] == "Alex Ivanovich"


@pytest.mark.asyncio
async def test_sort_projects_by_invalid_field(client):
    """
    Тест попытки сортировки по несуществующему полю.
    """
    response = client.get(
        "/projects", params={"sortBy": "invalid_field", "sortDir": "asc"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Поле 'invalid_field' не найдено"
