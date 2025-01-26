def test_create_customer(client):
    payload = {"name": "Ivan", "address": "test addres", "inn": "test inn"}
    response = client.post("/customers", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["name"] == "Ivan"
    assert result["address"] == "test addres"
    assert result["inn"] == "test inn"


def test_unauthenticated_user_cannot_create_object(client):
    client.headers = {}
    payload = {"name": "Ivan", "address": "test addres", "inn": "test inn"}
    response = client.post("/customers", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_cannot_create_customer_with_empty_field(client):
    payload = {}
    response = client.post("/customers", json=payload)
    assert response.status_code == 422
