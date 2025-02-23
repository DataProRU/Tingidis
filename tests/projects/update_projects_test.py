def test_update_project(
    client,
    sample_project,
    another_object,
    another_contract,
    another_user,
    another_project_status,
):
    project = sample_project
    payload = {
        "object": another_object.id,
        "contract": another_contract.id,
        "name": "test name2",
        "number": "2223",
        "main_executor": another_user.id,
        "deadline": "2024-12-12",
        "status": another_project_status.id,
        "notes": None,
    }
    response = client.patch(f"/projects/{project.id}", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["object"] == {
        "id": another_object.id,
        "code": another_object.code,
        "name": another_object.name,
        "comment": another_object.comment,
    }
    assert result["contract"] == {
        "id": another_contract.id,
        "code": another_contract.code,
        "name": another_contract.name,
        "customer": another_contract.customer,
        "executor": another_contract.executor,
        "number": another_contract.number,
        "sign_date": another_contract.sign_date.isoformat(),
        "price": float(another_contract.price),
        "theme": another_contract.theme,
        "evolution": another_contract.evolution,
    }
    assert result["name"] == "test name2"
    assert result["number"] == "2223"
    assert result["main_executor"] == {
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
    }
    assert result["deadline"] == "2024-12-12"
    assert result["status"] == {
        "id": another_project_status.id,
        "name": another_project_status.name,
    }
    assert result["notes"] is None


def test_unauthenticated_user_cannot_update_project(client, sample_project):
    client.headers = {}
    payload = {"name": "newtest object"}
    response = client.patch(f"/projects/{sample_project.id}", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
