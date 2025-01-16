def test_register_user(client):
    payload = {"username": "test2", "password": "test", "role": "admin"}
    response = client.post("/register", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["access_token"] is not None
    assert result["refresh_token"] is not None
    assert result["user"]["username"] == "test2"
    assert result["user"]["role"] == "admin"


def test_register_user_which_exists(client):
    payload = {"username": "user", "password": "test", "role": "admin"}
    response = client.post("/register", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "Пользователь существует"}


def test_register_with_empty_field(client):
    client.headers = {}
    payload = {"username": "user"}
    response = client.post("/register", json=payload)
    assert response.status_code == 422
