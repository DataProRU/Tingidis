def test_update_contacts(client, sample_contact, another_customer):
    payload = {
        "first_name": "Alex",
        "last_name": "Alexeev",
        "father_name": "Alexeevich",
        "phone": "+70000000002",
        "email": "alex@mail.com",
        "position": "engineer",
        "customer": another_customer.id,
    }
    response = client.patch(f"/contacts/{sample_contact.id}", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["first_name"] == "Alex"
    assert result["last_name"] == "Alexeev"
    assert result["father_name"] == "Alexeevich"
    assert result["phone"] == "+70000000002"
    assert result["email"] == "alex@mail.com"
    assert result["position"] == "engineer"
    assert result["customer"] == {
        "id": another_customer.id,
        "form": another_customer.form,
        "name": another_customer.name,
        "address": another_customer.address,
        "inn": another_customer.inn,
        "notes": another_customer.notes,
    }


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
        "customer": another_customer.id,
    }
    response = client.patch(f"/contacts/{sample_contact.id}", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
