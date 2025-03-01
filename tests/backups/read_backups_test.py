def test_get_empty_backups(client):
    response = client.get("/reserve-copies")
    assert response.status_code == 200
    assert response.json() == []


def test_unauthenticated_user_cannot_read_backups(client):
    client.headers = {}
    response = client.get("/reserve-copies")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_get_backups(client, sample_backup, another_backup):
    response = client.get("/reserve-copies")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": sample_backup.id,
            "email": sample_backup.email,
            "frequency": sample_backup.frequency,
            "send_date": sample_backup.send_date.isoformat(),
        },
        {
            "id": another_backup.id,
            "email": another_backup.email,
            "frequency": another_backup.frequency,
            "send_date": another_backup.send_date.isoformat(),
        },
    ]
