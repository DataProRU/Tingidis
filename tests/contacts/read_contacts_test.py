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
def test_get_contacts(client, sample_contact, another_contact):
    response = client.get(f"/contacts/")
    assert response.status_code == 200
    expected_result = [
        {
            "id": sample_contact.id,
            "first_name": sample_contact.first_name,
            "last_name": sample_contact.last_name,
            "father_name": sample_contact.father_name,
            "email": sample_contact.email,
            "position": sample_contact.position,
            "customer": 1,
        },
        {
            "id": another_contact.id,
            "first_name": another_contact.first_name,
            "last_name": another_contact.last_name,
            "father_name": another_contact.father_name,
            "email": another_contact.email,
            "position": another_contact.position,
            "customer": 2,
        },
    ]
    assert response.json() == expected_result


def test_get_contact(client, sample_contact):
    response = client.get(f"/contacts/{sample_contact.id}")
    assert response.status_code == 200
    expected_result = {
        "id": sample_contact.id,
        "first_name": sample_contact.first_name,
        "last_name": sample_contact.last_name,
        "father_name": sample_contact.father_name,
        "email": sample_contact.email,
        "position": sample_contact.position,
        "customer": 1,
    }
    assert response.json() == expected_result
