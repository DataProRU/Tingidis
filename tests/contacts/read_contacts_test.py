def test_get_empty_contacts(client):
    response = client.get("/contacts")
    assert response.status_code == 200
    assert response.json() == []


def test_unauthenticated_user_cannot_read_contacts(client):
    client.headers = {}
    response = client.get("/contacts")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


# Пример теста с использованием мока
def test_get_contacts(
    client, sample_contact, another_contact, sample_customer, another_customer
):
    response = client.get(f"/contacts/")
    assert response.status_code == 200
    expected_result = [
        {
            "id": sample_contact.id,
            "first_name": sample_contact.first_name,
            "last_name": sample_contact.last_name,
            "father_name": sample_contact.father_name,
            "phone": sample_contact.phone,
            "email": sample_contact.email,
            "position": sample_contact.position,
            "customer": {
                "id": sample_customer.id,
                "form": sample_customer.form,
                "name": sample_customer.name,
                "inn": sample_customer.inn,
                "address": sample_customer.address,
                "notes": sample_customer.notes,
            },
        },
        {
            "id": another_contact.id,
            "first_name": another_contact.first_name,
            "last_name": another_contact.last_name,
            "father_name": another_contact.father_name,
            "phone": another_contact.phone,
            "email": another_contact.email,
            "position": another_contact.position,
            "customer": {
                "id": another_customer.id,
                "form": another_customer.form,
                "name": another_customer.name,
                "inn": another_customer.inn,
                "address": another_customer.address,
                "notes": another_customer.notes,
            },
        },
    ]
    assert response.json() == expected_result


def test_get_contact(client, sample_contact, sample_customer):
    response = client.get(f"/contacts/{sample_contact.id}")
    assert response.status_code == 200
    expected_result = {
        "id": sample_contact.id,
        "first_name": sample_contact.first_name,
        "last_name": sample_contact.last_name,
        "father_name": sample_contact.father_name,
        "phone": sample_contact.phone,
        "email": sample_contact.email,
        "position": sample_contact.position,
        "customer": {
            "id": sample_customer.id,
            "form": sample_customer.form,
            "name": sample_customer.name,
            "inn": sample_customer.inn,
            "address": sample_customer.address,
            "notes": sample_customer.notes,
        },
    }
    assert response.json() == expected_result


def test_unauthenticated_user_cannot_read_contact(client, sample_contact):
    client.headers = {}
    response = client.get(f"/contacts/{sample_contact.id}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
