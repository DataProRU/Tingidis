def test_get_empty_customers(client):
    response = client.get("/customers")
    assert response.status_code == 200
    assert response.json() == []


def test_unauthenticated_user_cannot_read_customers(client):
    client.headers = {}
    response = client.get("/customers")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_get_customers(
    client,
    sample_customer,
    another_customer,
    sample_form,
    another_form,
    sample_contact,
    another_contact,
):
    customer_1 = sample_customer
    customer_2 = another_customer
    response = client.get("/customers")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": customer_1.id,
            "form": {"id": sample_form.id, "name": sample_form.name},
            "name": customer_1.name,
            "address": customer_1.address,
            "inn": customer_1.inn,
            "notes": customer_1.notes,
            "contacts": [
                {
                    "id": sample_contact.id,
                    "first_name": sample_contact.first_name,
                    "last_name": sample_contact.last_name,
                    "father_name": sample_contact.father_name,
                    "phone": sample_contact.phone,
                    "email": sample_contact.email,
                    "position": sample_contact.position,
                    "customer": sample_contact.customer,
                }
            ],
        },
        {
            "id": customer_2.id,
            "form": {"id": another_form.id, "name": another_form.name},
            "name": customer_2.name,
            "address": customer_2.address,
            "inn": customer_2.inn,
            "notes": customer_2.notes,
            "contacts": [
                {
                    "id": another_contact.id,
                    "first_name": another_contact.first_name,
                    "last_name": another_contact.last_name,
                    "father_name": another_contact.father_name,
                    "phone": another_contact.phone,
                    "email": another_contact.email,
                    "position": another_contact.position,
                    "customer": another_contact.customer,
                }
            ],
        },
    ]


def test_get_customer(client, sample_customer, sample_form, sample_contact):
    customer = sample_customer
    response = client.get(f"/customers/{customer.id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": customer.id,
        "form": {"id": sample_form.id, "name": sample_form.name},
        "name": customer.name,
        "address": customer.address,
        "inn": customer.inn,
        "notes": customer.notes,
        "contacts": [
            {
                "id": sample_contact.id,
                "first_name": sample_contact.first_name,
                "last_name": sample_contact.last_name,
                "father_name": sample_contact.father_name,
                "phone": sample_contact.phone,
                "email": sample_contact.email,
                "position": sample_contact.position,
                "customer": sample_contact.customer,
            }
        ],
    }


def test_unauthenticated_user_cannot_read_customer(client, sample_customer):
    client.headers = {}
    response = client.get(f"/customers/{sample_customer.id}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
