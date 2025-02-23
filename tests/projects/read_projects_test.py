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
    sample_project_executor,
):
    response = client.get(f"/projects/{sample_project.id}")
    assert response.status_code == 200

    expected_response = {
        "id": sample_project.id,
        "object": {
            "id": sample_object.id,
            "code": sample_object.code,
            "name": sample_object.name,
            "comment": sample_object.comment,
        },
        "contract": {
            "id": sample_contract.id,
            "code": sample_contract.code,
            "name": sample_contract.name,
            "customer": sample_contract.customer,
            "executor": sample_contract.executor,
            "number": sample_contract.number,
            "sign_date": sample_contract.sign_date.isoformat(),
            "price": float(sample_contract.price),
            "theme": sample_contract.theme,
            "evolution": sample_contract.evolution,
        },
        "name": sample_project.name,
        "number": sample_project.number,
        "main_executor": {
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
        "deadline": str(sample_project.deadline),
        "status": {"id": sample_project_status.id, "name": sample_project_status.name},
        "notes": sample_project.notes,
        "project_executors": [
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
        ],
    }

    assert response.json() == expected_response


def test_get_projects(
    client,
    sample_project,
    another_project,
    sample_object,
    another_object,
    sample_contract,
    another_contract,
    sample_user,
    another_user,
    sample_project_status,
    another_project_status,
    sample_project_executor,
    another_project_executor,
):
    response = client.get("/projects")
    assert response.status_code == 200

    expected_response = [
        {
            "id": sample_project.id,
            "object": {
                "id": sample_object.id,
                "code": sample_object.code,
                "name": sample_object.name,
                "comment": sample_object.comment,
            },
            "contract": {
                "id": sample_contract.id,
                "code": sample_contract.code,
                "name": sample_contract.name,
                "customer": sample_contract.customer,
                "executor": sample_contract.executor,
                "number": sample_contract.number,
                "sign_date": sample_contract.sign_date.isoformat(),
                "price": float(sample_contract.price),
                "theme": sample_contract.theme,
                "evolution": sample_contract.evolution,
            },
            "name": sample_project.name,
            "number": sample_project.number,
            "main_executor": {
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
            "deadline": str(sample_project.deadline),
            "status": {
                "id": sample_project_status.id,
                "name": sample_project_status.name,
            },
            "notes": sample_project.notes,
            "project_executors": [
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
                            sample_user.birthday.isoformat()
                            if sample_user.birthday
                            else None
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
                }
            ],
        },
        {
            "id": another_project.id,
            "object": {
                "id": another_object.id,
                "code": another_object.code,
                "name": another_object.name,
                "comment": another_object.comment,
            },
            "contract": None,
            "name": another_project.name,
            "number": another_project.number,
            "main_executor": {
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
                "notification": another_user.notification,
            },
            "deadline": str(another_project.deadline),
            "status": {
                "id": another_project_status.id,
                "name": another_project_status.name,
            },
            "notes": another_project.notes,
            "project_executors": [
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
                            another_user.birthday.isoformat()
                            if another_user.birthday
                            else None
                        ),
                        "category": another_user.category,
                        "specialization": another_user.specialization,
                        "username": another_user.username,
                        "password": None,
                        "notes": another_user.notes,
                        "role": another_user.role,
                        "notification": another_user.notification,
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
                }
            ],
        },
    ]

    assert response.json() == expected_response
