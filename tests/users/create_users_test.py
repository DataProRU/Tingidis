def test_create_user(client):
    payload = {
        "username": "user_alex",
        "password": "123456789qqFF_",
        "role": "user",
    }
    response = client.post("/users", json=payload)
    assert response.status_code == 403
    assert response.json() == {"detail": "Отсутствует доступ к запросу"}


def test_create_user_by_admin(admin_client):
    payload = {
        "username": "user_alex",
        "password": "123456789qqFF_",
        "role": "user",
    }
    response = admin_client.post("/users", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["username"] == "user_alex"
    assert result["password"] != "123456789qqFF_"
    assert result["role"] == "user"


def test_create_same_users(admin_client, sample_user):
    payload = {
        "username": sample_user.username,
        "password": sample_user.password,
        "role": sample_user.role,
    }

    # create the same user again
    response = admin_client.post("/users", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "Пользователь с таким username уже существует"}


def test_unauthenticated_user_cannot_create_user(client):
    client.headers = {}
    payload = {
        "username": "user_alex",
        "password": "123456789qqFF_",
        "role": "user",
    }
    response = client.post("/users", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_cannot_create_user_with_empty_field(client):
    payload = {"first_name": "Alex"}
    response = client.post("/users", json=payload)
    assert response.status_code == 422
