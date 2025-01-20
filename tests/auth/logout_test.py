import pytest


def test_logout_by_authorized(client, sample_user):
    user = sample_user
    client.headers = {}
    payload = {
        "username": user.username,
        "password": "123456789",
    }
    response = client.post("/login", json=payload)
    assert response.status_code == 200
    response = client.post("/logout", json=payload)
    assert response.status_code == 200
    assert response.json()["refresh_token"] is not None


def test_logout_by_unauthorized(client):
    response = client.post("/logout")
    assert response.status_code == 200
    assert response.json()["refresh_token"] is None
