import pytest


@pytest.mark.skip(reason="TODO")
def test_register_user_which_exists(client):
    payload = {"username": "user", "password": "test", "role": "admin"}
    response = client.post("/register", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "Пользователь существует"}


@pytest.mark.skip(reason="TODO")
def test_register_user(client):
    client.headers = {}
    payload = {"username": "test4", "password": "test", "role": "admin"}
    response = client.post("/register", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["access_token"] is not None
    assert result["refresh_token"] is not None
    assert result["user"]["username"] == "test4"
    assert result["user"]["role"] == "admin"
