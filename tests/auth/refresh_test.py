def test_refresh(client, sample_user):
    user = sample_user
    client.headers = {}
    payload = {
        "username": user.username,
        "password": "123456789",
    }
    response = client.post("/login", json=payload)
    assert response.status_code == 200
    response = client.get("/refresh")
    assert response.status_code == 200
    result = response.json()
    assert result["access_token"] is not None
    assert result["refresh_token"] is not None
    assert result["user"]["id"] == user.id
    assert result["user"]["username"] == user.username
    assert result["user"]["role"] == user.role


def test_refresh_by_unauthorized(client):
    response = client.get("/refresh")
    assert response.status_code == 401
    assert response.json() == {"detail": "Пользователь не авторизован"}
