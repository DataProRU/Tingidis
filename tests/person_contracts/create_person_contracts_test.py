def test_create_person_contract(client, another_customer):
    payload = {
        "first_name": "Alex",
        "last_name": "Alexeev",
        "father_name": "Alexeevich",
        "email": "alex@mail.com",
        "position": "engineer",
        "customer": str(another_customer.id),
    }
    response = client.post("/person-contracts", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["first_name"] == "Alex"
    assert result["last_name"] == "Alexeev"
    assert result["father_name"] == "Alexeevich"
    assert result["email"] == "alex@mail.com"
    assert result["position"] == "engineer"
    assert result["customer"] == another_customer.id


def test_unauthenticated_user_cannot_create_person_contracts(client, another_customer):
    client.headers = {}
    payload = {
        "first_name": "Alex",
        "last_name": "Alexeev",
        "father_name": "Alexeevich",
        "email": "aled@mail.com",
        "position": "engineer",
        "customer": str(another_customer.id),
    }
    response = client.post("/person-contracts", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_cannot_create_object_with_empty_field(client):
    payload = {
        "first_name": "Alex",
        "last_name": "Alexeev",
        "father_name": "Alexeevich",
        "email": "aled@mail.com",
        "position": "engineer",
    }
    response = client.post("/person-contracts", json=payload)
    assert response.status_code == 422
