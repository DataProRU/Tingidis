from datetime import datetime


def test_create_contract(client, sample_object):
    payload = {
        "code": sample_object.id,
        "name": "Sample Contract",
        "number": "1234567890",
        "sign_date": datetime(2024, 2, 2).date().isoformat(),
        "price": 2000.21,
        "theme": "Sample Theme",
        "evolution": "Sample Evolution",
    }
    response = client.post("/contracts", json=payload)
    assert response.status_code == 201

    # Проверка ответа
    response_data = response.json()
    assert response_data["code"] == sample_object.id
    assert response_data["name"] == "Sample Contract"
    assert response_data["number"] == "1234567890"
    assert response_data["sign_date"] == datetime(2024, 2, 2).date().isoformat()
    assert response_data["price"] == 2000.21
    assert response_data["theme"] == "Sample Theme"
    assert response_data["evolution"] == "Sample Evolution"


def test_unauthenticated_user_cannot_create_contract(client, sample_object):
    client.headers = {}
    payload = {
        "code": sample_object.id,
        "name": "Sample Contract",
        "number": "1234567890",
        "sign_date": datetime(2024, 2, 2).date().isoformat(),
        "price": 2000.21,
        "theme": "Sample Theme",
        "evolution": "Sample Evolution",
    }
    response = client.post("/contracts", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_cannot_create_object_with_empty_field(client, sample_object):
    payload = {
        "code": sample_object.id,
        "name": "Sample Contract",
        "number": "1234567890",
    }
    response = client.post("/contracts", json=payload)
    assert response.status_code == 422
