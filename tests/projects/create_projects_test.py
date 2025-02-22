from datetime import date


def test_create_project(
    client, sample_object, sample_contract, sample_user, sample_project_status
):
    payload = {
        "object": sample_object.id,
        "contract": sample_contract.id,
        "name": "test name",
        "number": "222",
        "main_executor": sample_user.id,
        "deadline": date.today().isoformat(),
        "status": sample_project_status.id,
        "notes": "test notes",
    }

    response = client.post("/projects", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["object"] == sample_object.id
    assert result["contract"] == sample_contract.id
    assert result["name"] == "test name"
    assert result["number"] == "222"
    assert result["main_executor"] == sample_user.id
    assert result["deadline"] == date.today().isoformat()
    assert result["status"] == sample_object.id
    assert result["notes"] == "test notes"


def test_unauthenticated_user_cannot_create_projects(
    client, sample_object, sample_contract, sample_user, sample_project_status
):
    client.headers = {}
    payload = {
        "object": sample_object.id,
        "contract": sample_contract.id,
        "name": "test name",
        "number": "222",
        "main_executor": sample_user.id,
        "deadline": date.today().isoformat(),
        "status": sample_project_status.id,
        "notes": "test notes",
    }
    response = client.post("/projects", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_cannot_create_projects_with_empty_fields(
    client, sample_object, sample_contract, sample_user
):
    payload = {
        "object": sample_object.id,
        "contract": sample_contract.id,
        "name": "test name",
        "number": "222",
        "main_executor": sample_user.id,
        "notes": "test notes",
    }
    response = client.post("/projects", json=payload)
    assert response.status_code == 422
