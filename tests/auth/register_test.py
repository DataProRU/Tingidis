def test_register_user(client):
    payload = {
        "username": "test2",
        "first_name": "Alex",
        "last_name": "Brown",
        "password": "test",
        "role": "admin",
    }
    response = client.post("/register", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["access_token"] is not None
    assert result["refresh_token"] is not None
    assert result["user"]["username"] == "test2"
    assert result["user"]["first_name"] == "Alex"
    assert result["user"]["last_name"] == "Brown"
    assert result["user"]["role"] == "admin"


def test_register_user_which_exists(client):
    payload = {
        "username": "user 1",
        "first_name": "Alex",
        "last_name": "Brown",
        "password": "test",
        "role": "admin",
    }
    response = client.post("/register", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "Пользователь существует"}


def test_register_with_empty_field(client):
    client.headers = {}
    payload = {"username": "user"}
    response = client.post("/register", json=payload)
    assert response.status_code == 422
