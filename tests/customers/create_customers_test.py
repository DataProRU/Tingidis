from web_app.models.contacts import Contacts


def test_create_customer(client, sample_form):
    payload = {
        "name": "Ivan",
        "form": sample_form.id,
        "address": "test addres",
        "inn": "test inn",
        "notes": "test note",
    }
    response = client.post("/customers", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["name"] == "Ivan"
    assert result["form"] == sample_form.id
    assert result["address"] == "test addres"
    assert result["inn"] == "test inn"
    assert result["notes"] == "test note"


def test_create_customer_with_contact(client, sample_form):
    payload = {
        "name": "Ivan",
        "form": sample_form.id,
        "address": "test address",
        "inn": "test inn",
        "notes": "test note",
        "contacts": [
            {
                "first_name": "John",
                "last_name": "Doe",
                "father_name": "Smith",
                "phone": "1234567890",
                "email": "john.doe@example.com",
                "position": "Manager",
            },
            {
                "first_name": "Jane",
                "last_name": "Doe",
                "father_name": "Ann",
                "phone": "0987654321",
                "email": "jane.doe@example.com",
                "position": "Assistant",
            },
        ],
    }

    response = client.post("/customers", json=payload)

    assert response.status_code == 201
    result = response.json()

    assert result["name"] == "Ivan"
    assert result["form"] == sample_form.id
    assert result["address"] == "test address"
    assert result["inn"] == "test inn"
    assert result["notes"] == "test note"

    assert "contacts" in result
    assert len(result["contacts"]) == 2
    assert result["contacts"][0]["first_name"] == "John"
    assert result["contacts"][0]["last_name"] == "Doe"
    assert result["contacts"][0]["father_name"] == "Smith"
    assert result["contacts"][0]["phone"] == "1234567890"
    assert result["contacts"][0]["email"] == "john.doe@example.com"
    assert result["contacts"][0]["position"] == "Manager"

    assert result["contacts"][1]["first_name"] == "Jane"
    assert result["contacts"][1]["last_name"] == "Doe"
    assert result["contacts"][1]["father_name"] == "Ann"
    assert result["contacts"][1]["phone"] == "0987654321"
    assert result["contacts"][1]["email"] == "jane.doe@example.com"
    assert result["contacts"][1]["position"] == "Assistant"


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
