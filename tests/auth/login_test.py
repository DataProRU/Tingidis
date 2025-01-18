def test_login_user(client, sample_user):
    user = sample_user
    client.headers = {}
    payload = {
        "username": user.username,
        "password": "123456789",
    }
    response = client.post("/login", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["access_token"] is not None
    assert result["refresh_token"] is not None
    assert result["user"]["id"] == user.id
    assert result["user"]["username"] == user.username
    assert result["user"]["role"] == user.role


def test_login_with_incorrect_data(client):
    client.headers = {}
    payload = {
        "username": "user",
        "password": "1234567810",
    }
    response = client.post("/login", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Неверный логин или пароль"}


def test_login_with_empty_field(client):
    client.headers = {}
    payload = {"username": "user"}
    response = client.post("/login", json=payload)
    assert response.status_code == 422
