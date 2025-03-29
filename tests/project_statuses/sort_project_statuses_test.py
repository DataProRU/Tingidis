import pytest


@pytest.mark.asyncio
async def test_sort_project_statuses_by_name_asc(
    client, sample_project_status, another_project_status, in_progress_status
):
    """
    Тест сортировки статусов проектов по имени в порядке возрастания.
    """
    response = client.get(
        "/project-statuses", params={"sortBy": "name", "sortDir": "asc"}
    )
    assert response.status_code == 200

    statuses = response.json()
    assert len(statuses) >= 3
    assert statuses[0]["name"] == "another status"
    assert statuses[1]["name"] == "In Progress"
    assert statuses[2]["name"] == "sample status"


@pytest.mark.asyncio
async def test_sort_project_statuses_by_name_desc(
    client, sample_project_status, another_project_status, in_progress_status
):
    """
    Тест сортировки статусов проектов по имени в порядке убывания.
    """
    response = client.get(
        "/project-statuses", params={"sortBy": "name", "sortDir": "desc"}
    )
    assert response.status_code == 200

    statuses = response.json()
    assert len(statuses) >= 3
    assert statuses[0]["name"] == "sample status"
    assert statuses[1]["name"] == "In Progress"
    assert statuses[2]["name"] == "another status"


@pytest.mark.asyncio
async def test_sort_project_statuses_by_invalid_field(client):
    """
    Тест попытки сортировки по несуществующему полю.
    """
    response = client.get(
        "/project-statuses", params={"sortBy": "invalid_field", "sortDir": "asc"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Поле не найдено"
