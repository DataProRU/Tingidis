def test_get_empty_project_statuses(client):
    response = client.get("/project-statuses")
    assert response.status_code == 200
    assert response.json() == []


def test_unauthenticated_user_cannot_read_project_statuses(client):
    client.headers = {}
    response = client.get("/project-statuses")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_get_project_statuses(client, sample_project_status, another_project_status):
    response = client.get("/project-statuses")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": sample_project_status.id,
            "name": sample_project_status.name,
        },
        {
            "id": another_project_status.id,
            "name": another_project_status.name,
        },
    ]


def test_get_project_status(client, sample_project_status):
    response = client.get(f"/project-statuses/{sample_project_status.id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": sample_project_status.id,
        "name": sample_project_status.name,
    }


def test_unauthenticated_user_cannot_read_project_status_by_id(
    client, sample_project_status
):
    client.headers = {}
    response = client.get(f"/project-statuses/{sample_project_status.id}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
