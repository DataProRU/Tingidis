from datetime import datetime


def test_create_contracts(client, sample_object, sample_customer, sample_user):
    payload = {
        "code": sample_object.id,
        "name": "test name",
        "customer": sample_customer.id,
        "executor": sample_user.id,
        "number": "string",
        "sign_date": str(datetime.today().strftime("%Y-%m-%d")),
        "price": 1000,
        "theme": "test theme",
        "evolution": "test string",
    }
    response = client.post("/contracts", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["code"] == sample_object.id
    assert result["name"] == "test name"
    assert result["customer"] == sample_customer.id
    assert result["executor"] == sample_user.id
    assert result["sign_date"] == datetime.today().strftime("%Y-%m-%d")
    assert result["price"] == 1000
    assert result["theme"] == "test theme"
    assert result["evolution"] == "test string"


def test_unauthenticated_user_cannot_create_contracts(
    client, sample_object, sample_customer, sample_user
):
    client.headers = {}
    payload = {
        "code": sample_object.id,
        "name": "test name",
        "customer": sample_customer.id,
        "executor": sample_user.id,
        "number": "string",
        "sign_date": "2025-02-09",
        "price": 1000,
        "theme": "test theme",
        "evolution": "test string",
    }
    response = client.post("/contracts", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_cannot_create_contracts_with_empty_field(
    client,
    sample_object,
):
    payload = {
        "code": str(sample_object.id),
    }
    response = client.post("/contracts", json=payload)
    assert response.status_code == 422
