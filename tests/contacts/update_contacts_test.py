def test_update_contacts(client, sample_contact, another_customer):
    payload = {
        "first_name": "Alex",
        "last_name": "Alexeev",
        "father_name": "Alexeevich",
        "email": "alex@mail.com",
        "position": "engineer",
        "customer": str(another_customer.id),
    }
    response = client.patch(f"/contacts/{sample_contact.id}", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["first_name"] == "Alex"
    assert result["last_name"] == "Alexeev"
    assert result["father_name"] == "Alexeevich"
    assert result["email"] == "alex@mail.com"
    assert result["position"] == "engineer"
    assert result["customer"] == another_customer.id


def test_unauthenticated_user_cannot_update_contact(
    client, sample_contact, another_customer
):
    client.headers = {}
    payload = {
        "first_name": "Alex",
        "last_name": "Alexeev",
        "father_name": "Alexeevich",
        "email": "aled@mail.com",
        "position": "engineer",
        "customer": str(another_customer.id),
    }
    response = client.patch(f"/contacts/{sample_contact.id}", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
