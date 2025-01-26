def test_get_empty_customers(client):
    response = client.get("/customers")
    assert response.status_code == 200
    assert response.json() == []


def test_unauthenticated_user_cannot_read_customers(client):
    client.headers = {}
    response = client.get("/customers")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_get_customers(client, sample_customer, another_customer):
    customer_1 = sample_customer
    customer_2 = another_customer
    response = client.get("/customers")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": customer_1.id,
            "name": customer_1.name,
            "address": customer_1.address,
            "inn": customer_1.inn,
        },
        {
            "id": customer_2.id,
            "name": customer_2.name,
            "address": customer_2.address,
            "inn": customer_2.inn,
        },
    ]


def test_get_object(client, sample_customer):
    customer = sample_customer
    response = client.get(f"/customers/{customer.id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": customer.id,
        "name": customer.name,
        "address": customer.address,
        "inn": customer.inn,
    }
