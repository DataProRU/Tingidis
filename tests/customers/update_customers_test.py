def test_update_customer(client, sample_customer):
    customer = sample_customer
    payload = {"name": "new Ivan", "address": "new test addres", "inn": "new test inn"}
    response = client.patch(f"/customers/{customer.id}", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "new Ivan"
    assert result["address"] == "new test addres"
    assert result["inn"] == "new test inn"


def test_unauthenticated_user_cannot_update_customer(client, sample_customer):
    object = sample_customer
    client.headers = {}
    payload = {"name": "new Ivan", "address": "new test address", "inn": "new test inn"}
    response = client.patch(f"/customers/{object.id}", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
