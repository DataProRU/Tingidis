def test_filters_customers(
    client,
    sample_customer,
    another_customer,
    third_customer,
    sample_form,
    another_form,
    third_form,
    sample_contact,
    another_contact,
):

    response = client.get(
        "/customers", params={"form": [sample_form.name, another_form.name]}
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": sample_customer.id,
            "form": (
                {
                    "id": sample_form.id,
                    "name": sample_form.name,
                }
            ),
            "name": sample_customer.name,
            "address": sample_customer.address,
            "inn": sample_customer.inn,
            "notes": sample_customer.notes,
            "contacts": [
                {
                    "customer": sample_customer.id,
                    "email": sample_contact.email,
                    "father_name": sample_contact.father_name,
                    "first_name": sample_contact.first_name,
                    "id": sample_contact.id,
                    "last_name": sample_contact.last_name,
                    "phone": sample_contact.phone,
                    "position": sample_contact.position,
                }
            ],
        },
        {
            "id": another_customer.id,
            "form": (
                {
                    "id": another_form.id,
                    "name": another_form.name,
                }
            ),
            "name": another_customer.name,
            "address": another_customer.address,
            "inn": another_customer.inn,
            "notes": another_customer.notes,
            "contacts": [
                {
                    "customer": another_contact.id,
                    "email": another_contact.email,
                    "father_name": another_contact.father_name,
                    "first_name": another_contact.first_name,
                    "id": another_contact.id,
                    "last_name": another_contact.last_name,
                    "phone": another_contact.phone,
                    "position": another_contact.position,
                }
            ],
        },
    ]

    response = client.get(
        "/customers", params={"name": [sample_customer.name, another_customer.name]}
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": sample_customer.id,
            "form": (
                {
                    "id": sample_form.id,
                    "name": sample_form.name,
                }
            ),
            "name": sample_customer.name,
            "address": sample_customer.address,
            "inn": sample_customer.inn,
            "notes": sample_customer.notes,
            "contacts": [
                {
                    "customer": sample_customer.id,
                    "email": sample_contact.email,
                    "father_name": sample_contact.father_name,
                    "first_name": sample_contact.first_name,
                    "id": sample_contact.id,
                    "last_name": sample_contact.last_name,
                    "phone": sample_contact.phone,
                    "position": sample_contact.position,
                }
            ],
        },
        {
            "id": another_customer.id,
            "form": (
                {
                    "id": another_form.id,
                    "name": another_form.name,
                }
            ),
            "name": another_customer.name,
            "address": another_customer.address,
            "inn": another_customer.inn,
            "notes": another_customer.notes,
            "contacts": [
                {
                    "customer": another_contact.id,
                    "email": another_contact.email,
                    "father_name": another_contact.father_name,
                    "first_name": another_contact.first_name,
                    "id": another_contact.id,
                    "last_name": another_contact.last_name,
                    "phone": another_contact.phone,
                    "position": another_contact.position,
                }
            ],
        },
    ]

    response = client.get(
        "/customers",
        params={"address": [sample_customer.address, another_customer.address]},
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": sample_customer.id,
            "form": (
                {
                    "id": sample_form.id,
                    "name": sample_form.name,
                }
            ),
            "name": sample_customer.name,
            "address": sample_customer.address,
            "inn": sample_customer.inn,
            "notes": sample_customer.notes,
            "contacts": [
                {
                    "customer": sample_customer.id,
                    "email": sample_contact.email,
                    "father_name": sample_contact.father_name,
                    "first_name": sample_contact.first_name,
                    "id": sample_contact.id,
                    "last_name": sample_contact.last_name,
                    "phone": sample_contact.phone,
                    "position": sample_contact.position,
                }
            ],
        },
        {
            "id": another_customer.id,
            "form": (
                {
                    "id": another_form.id,
                    "name": another_form.name,
                }
            ),
            "name": another_customer.name,
            "address": another_customer.address,
            "inn": another_customer.inn,
            "notes": another_customer.notes,
            "contacts": [
                {
                    "customer": another_contact.id,
                    "email": another_contact.email,
                    "father_name": another_contact.father_name,
                    "first_name": another_contact.first_name,
                    "id": another_contact.id,
                    "last_name": another_contact.last_name,
                    "phone": another_contact.phone,
                    "position": another_contact.position,
                }
            ],
        },
    ]

    response = client.get(
        "/customers", params={"inn": [sample_customer.inn, another_customer.inn]}
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": sample_customer.id,
            "form": (
                {
                    "id": sample_form.id,
                    "name": sample_form.name,
                }
            ),
            "name": sample_customer.name,
            "address": sample_customer.address,
            "inn": sample_customer.inn,
            "notes": sample_customer.notes,
            "contacts": [
                {
                    "customer": sample_customer.id,
                    "email": sample_contact.email,
                    "father_name": sample_contact.father_name,
                    "first_name": sample_contact.first_name,
                    "id": sample_contact.id,
                    "last_name": sample_contact.last_name,
                    "phone": sample_contact.phone,
                    "position": sample_contact.position,
                }
            ],
        },
        {
            "id": another_customer.id,
            "form": (
                {
                    "id": another_form.id,
                    "name": another_form.name,
                }
            ),
            "name": another_customer.name,
            "address": another_customer.address,
            "inn": another_customer.inn,
            "notes": another_customer.notes,
            "contacts": [
                {
                    "customer": another_contact.id,
                    "email": another_contact.email,
                    "father_name": another_contact.father_name,
                    "first_name": another_contact.first_name,
                    "id": another_contact.id,
                    "last_name": another_contact.last_name,
                    "phone": another_contact.phone,
                    "position": another_contact.position,
                }
            ],
        },
    ]

    response = client.get(
        "/customers", params={"notes": [sample_customer.notes, another_customer.notes]}
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": another_customer.id,
            "form": (
                {
                    "id": another_form.id,
                    "name": another_form.name,
                }
            ),
            "name": another_customer.name,
            "address": another_customer.address,
            "inn": another_customer.inn,
            "notes": another_customer.notes,
            "contacts": [
                {
                    "customer": another_contact.id,
                    "email": another_contact.email,
                    "father_name": another_contact.father_name,
                    "first_name": another_contact.first_name,
                    "id": another_contact.id,
                    "last_name": another_contact.last_name,
                    "phone": another_contact.phone,
                    "position": another_contact.position,
                }
            ],
        },
        {
            "id": third_customer.id,
            "form": (
                {
                    "id": third_form.id,
                    "name": third_form.name,
                }
            ),
            "name": third_customer.name,
            "address": third_customer.address,
            "inn": third_customer.inn,
            "notes": third_customer.notes,
            "contacts": [],
        },
    ]
