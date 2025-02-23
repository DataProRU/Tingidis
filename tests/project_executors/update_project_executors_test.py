def test_update_project_executor(
    client,
    sample_project_executor,
    another_user,
    another_project,
):
    project_executor = sample_project_executor
    payload = {
        "user": another_user.id,
        "project": another_project.id,
    }

    response = client.patch(f"/project-executors/{project_executor.id}", json=payload)
    assert response.status_code == 200
    result = response.json()

    assert result["user"] == {
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
    assert result["project"] == {
        "id": another_project.id,
        "object": another_project.object,
        "contract": another_project.contract,
        "name": another_project.name,
        "number": another_project.number,
        "main_executor": another_project.main_executor,
        "deadline": str(another_project.deadline),
        "status": another_project.status,
        "notes": another_project.notes,
    }


def test_unauthenticated_user_cannot_update_project_executors(
    client, sample_project_executor, another_user, another_project
):
    client.headers = {}
    payload = {
        "user": another_user.id,
        "project": another_project.id,
    }
    response = client.patch(
        f"/project-executors/{sample_project_executor.id}", json=payload
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
