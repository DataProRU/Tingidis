def test_create_object(client):
    payload = {"code": "123456", "name": "test object"}
    response = client.post("/objects", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["code"] == "123456"
    assert result["name"] == "test object"
    assert result["comment"] is None


def test_create_object_with_wrong_code(client, sample_object):
    payload = {"code": sample_object.code, "name": sample_object.name}
    response = client.post("/objects", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "Обьект с таким кодом уже существует"}


def test_unauthenticated_user_cannot_create_object(client):
    client.headers = {}
    payload = {"code": "123456", "name": "test object"}
    response = client.post("/objects", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_cannot_create_object_with_empty_field(client):
    payload = {
        "code": "123456",
    }
    response = client.post("/objects", json=payload)
    assert response.status_code == 422
