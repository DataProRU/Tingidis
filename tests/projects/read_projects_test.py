def test_get_empty_projects(client):
    response = client.get("/projects")
    assert response.status_code == 200
    assert response.json() == []


def test_unauthenticated_user_cannot_read_projects(client):
    client.headers = {}
    response = client.get("/projects")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_unauthenticated_user_cannot_read_project_by_id(client, sample_project):
    client.headers = {}
    response = client.get(f"/projects/{sample_project.id}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_get_project(
    client,
    sample_project,
    sample_object,
    sample_contract,
    sample_user,
    sample_project_status,
):
    response = client.get(f"/projects/{sample_project.id}")
    assert response.status_code == 200

    expected_response = {
        "id": None,
        "object": {
            "id": sample_object.id,
            "code": sample_object.code,
            "name": sample_object.name,
            "comment": sample_object.comment,
        },
        "contract": {
            "id": sample_contract.id,
            "first_name": "",
            "last_name": "",
            "father_name": "",
            "phone": "",
            "email": "",
            "position": "",
            "customer": sample_contract.customer,
        },
        "name": sample_project.name,
        "number": sample_project.number,
        "project_main_executor": {
            "id": sample_user.id,
            "first_name": sample_user.first_name,
            "last_name": sample_user.last_name,
            "father_name": sample_user.father_name,
            "full_name": sample_user.full_name,
            "position": sample_user.position,
            "phone": sample_user.phone,
            "email": sample_user.email,
            "telegram": sample_user.telegram,
            "birthday": sample_user.birthday,
            "category": sample_user.category,
            "specialization": sample_user.specialization,
            "username": sample_user.username,
            "password": None,
            "notes": sample_user.notes,
            "role": sample_user.role,
        },
        "deadline": str(sample_project.deadline),
        "status": {"id": sample_project_status.id, "name": sample_project_status.name},
        "notes": sample_project.notes,
        "project_executors": [],
    }

    assert response.json() == expected_response
