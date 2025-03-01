from datetime import datetime, timedelta


def test_create_backup(client):
    payload = {
        "email": "test@gmail.com",
        "frequency": 2,
    }
    response = client.post("/reserve-copies", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["email"] == "test@gmail.com"
    assert result["frequency"] == 2
    assert result["send_date"] == (datetime.now() + timedelta(days=7)).strftime(
        "%Y-%m-%d"
    )


def test_unauthenticated_user_cannot_backup(client):
    client.headers = {}
    payload = {
        "email": "test@gmail.com",
        "frequency": 2,
    }
    response = client.post("/reserve-copies", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_cannot_create_backup_with_empty_field(client):
    payload = {
        "frequency": 2,
    }
    response = client.post("/reserve-copies", json=payload)
    assert response.status_code == 422
