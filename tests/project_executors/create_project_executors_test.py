def test_project_executor(client, sample_project, another_user):
    payload = {
        "user": another_user.id,
        "project": sample_project.id,
    }

    response = client.post("/project-executors", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["user"] == another_user.id
    assert result["project"] == sample_project.id


def test_project_executor_cant_be_main_executor(client, sample_project, sample_user):
    payload = {
        "user": sample_user.id,
        "project": sample_project.id,
    }

    response = client.post("/project-executors", json=payload)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Исполнитель не может быть основным ответственным за проект"
    }


def test_project_executor_cant_be_added_two_times(client, sample_project, another_user):
    payload = {
        "user": another_user.id,
        "project": sample_project.id,
    }

    response = client.post("/project-executors", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["user"] == another_user.id
    assert result["project"] == sample_project.id

    response = client.post("/project-executors", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "Исполнитель уже добавлен на проект"}


def test_unauthenticated_user_cannot_create_project_executor(
    client, sample_project, sample_user
):
    client.headers = {}
    payload = {
        "user": sample_user.id,
        "project": sample_project.id,
    }

    response = client.post("/project-executors", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_cannot_create_project_executor_with_empty_fields(client, sample_user):
    payload = {
        "user": sample_user.id,
    }

    response = client.post("/project-executors", json=payload)
    assert response.status_code == 422
