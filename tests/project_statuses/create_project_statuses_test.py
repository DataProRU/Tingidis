def test_create_project_status(client):
    payload = {"name": "test project status name"}
    response = client.post("/project-statuses", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["name"] == "test project status name"


def test_unauthenticated_user_cannot_create_project_status(client):
    client.headers = {}
    payload = {"name": "test project status name"}
    response = client.post("/project-statuses", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_cannot_create_project_status_with_empty_field(client):
    payload = {}
    response = client.post("/project-statuses", json=payload)
    assert response.status_code == 422
