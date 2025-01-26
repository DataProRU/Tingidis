def test_create_form(client):
    payload = {"name": "test form"}
    response = client.post("/form-of-ownership", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["name"] == "test form"


def test_unauthenticated_user_cannot_create_form(client):
    client.headers = {}
    payload = {"name": "test object"}
    response = client.post("/form-of-ownership", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_cannot_create_object_with_empty_field(client):
    payload = {}
    response = client.post("/form-of-ownership", json=payload)
    assert response.status_code == 422
