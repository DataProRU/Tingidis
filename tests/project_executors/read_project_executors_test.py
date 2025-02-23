def test_get_empty_project_executors(client):
    response = client.get("/project-executors")
    assert response.status_code == 200
    assert response.json() == []


def test_unauthenticated_user_cannot_read_project_executors(client):
    client.headers = {}
    response = client.get("/project-executors")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_unauthenticated_user_cannot_read_project_executor_by_id(
    client, sample_project_executor
):
    client.headers = {}
    response = client.get(f"/project-executors/{sample_project_executor.id}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_get_project_executor(
    client, sample_project_executor, sample_project, sample_user
):
    response = client.get(f"/project-executors/{sample_project_executor.id}")
    assert response.status_code == 200

    expected_response = {
        "id": sample_project_executor.id,
        "user": {
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
            "notification": sample_user.notification,
        },
        "project": {
            "id": sample_project.id,
            "object": sample_project.object,
            "contract": sample_project.contract,
            "name": sample_project.name,
            "number": sample_project.number,
            "main_executor": sample_project.main_executor,
            "deadline": str(sample_project.deadline),
            "status": sample_project.status,
            "notes": sample_project.notes,
        },
    }

    assert response.json() == expected_response


def test_get_project_executors(
    client,
    sample_project_executor,
    another_project_executor,
    sample_project,
    another_project,
    sample_user,
    another_user,
):
    response = client.get(f"/project-executors")
    assert response.status_code == 200

    expected_response = [
        {
            "id": sample_project_executor.id,
            "user": {
                "id": sample_user.id,
                "first_name": sample_user.first_name,
                "last_name": sample_user.last_name,
                "father_name": sample_user.father_name,
                "full_name": sample_user.full_name,
                "position": sample_user.position,
                "phone": sample_user.phone,
                "email": sample_user.email,
                "telegram": sample_user.telegram,
                "birthday": (
                    sample_user.birthday.isoformat() if sample_user.birthday else None
                ),
                "category": sample_user.category,
                "specialization": sample_user.specialization,
                "username": sample_user.username,
                "password": None,
                "notes": sample_user.notes,
                "role": sample_user.role,
                "notification": sample_user.notification,
            },
            "project": {
                "id": sample_project.id,
                "object": sample_project.object,
                "contract": sample_project.contract,
                "name": sample_project.name,
                "number": sample_project.number,
                "main_executor": sample_project.main_executor,
                "deadline": str(sample_project.deadline),
                "status": sample_project.status,
                "notes": sample_project.notes,
            },
        },
        {
            "id": another_project_executor.id,
            "user": {
                "id": another_user.id,
                "first_name": another_user.first_name,
                "last_name": another_user.last_name,
                "father_name": another_user.father_name,
                "full_name": another_user.full_name,
                "position": another_user.position,
                "phone": another_user.phone,
                "email": another_user.email,
                "telegram": another_user.telegram,
                "birthday": (
                    another_user.birthday.isoformat() if another_user.birthday else None
                ),
                "category": another_user.category,
                "specialization": another_user.specialization,
                "username": another_user.username,
                "password": None,
                "notes": another_user.notes,
                "role": another_user.role,
                "notification": sample_user.notification,
            },
            "project": {
                "id": another_project.id,
                "object": another_project.object,
                "contract": another_project.contract,
                "name": another_project.name,
                "number": another_project.number,
                "main_executor": another_project.main_executor,
                "deadline": str(another_project.deadline),
                "status": another_project.status,
                "notes": another_project.notes,
            },
        },
    ]

    assert response.json() == expected_response
