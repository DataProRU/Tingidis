def test_filters_contacts(
    client,
    sample_contact,
    another_contact,
    third_contact,
    sample_customer,
    another_customer,
    third_customer,
    fourth_contact,
    fouth_customer,
):
    response = client.get(
        "/contacts",
        params={"first_name": [sample_contact.first_name, another_contact.first_name]},
    )
    assert response.status_code == 200
    assert response.json() == [
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

    response = client.get(
        "/contacts",
        params={"last_name": [sample_contact.last_name, third_contact.last_name]},
    )
    assert response.status_code == 200
    assert response.json() == [
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
            "id": third_contact.id,
            "first_name": third_contact.first_name,
            "last_name": third_contact.last_name,
            "father_name": third_contact.father_name,
            "phone": third_contact.phone,
            "email": third_contact.email,
            "position": third_contact.position,
            "customer": {
                "id": third_customer.id,
                "form": third_customer.form,
                "name": third_customer.name,
                "inn": third_customer.inn,
                "address": third_customer.address,
                "notes": third_customer.notes,
            },
        },
    ]

    response = client.get(
        "/contacts",
        params={
            "father_name": [another_contact.father_name, third_contact.father_name]
        },
    )
    assert response.status_code == 200
    assert response.json() == [
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
        {
            "id": third_contact.id,
            "first_name": third_contact.first_name,
            "last_name": third_contact.last_name,
            "father_name": third_contact.father_name,
            "phone": third_contact.phone,
            "email": third_contact.email,
            "position": third_contact.position,
            "customer": {
                "id": third_customer.id,
                "form": third_customer.form,
                "name": third_customer.name,
                "inn": third_customer.inn,
                "address": third_customer.address,
                "notes": third_customer.notes,
            },
        },
    ]

    response = client.get(
        "/contacts", params={"email": [another_contact.email, sample_contact.email]}
    )
    assert response.status_code == 200
    assert response.json() == [
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

    response = client.get(
        "/contacts", params={"phone": [third_contact.phone, sample_contact.phone]}
    )
    assert response.status_code == 200
    assert response.json() == [
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
            "id": third_contact.id,
            "first_name": third_contact.first_name,
            "last_name": third_contact.last_name,
            "father_name": third_contact.father_name,
            "phone": third_contact.phone,
            "email": third_contact.email,
            "position": third_contact.position,
            "customer": {
                "id": third_customer.id,
                "form": third_customer.form,
                "name": third_customer.name,
                "inn": third_customer.inn,
                "address": third_customer.address,
                "notes": third_customer.notes,
            },
        },
    ]

    response = client.get(
        "/contacts",
        params={"position": [third_contact.position, fourth_contact.position]},
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": third_contact.id,
            "first_name": third_contact.first_name,
            "last_name": third_contact.last_name,
            "father_name": third_contact.father_name,
            "phone": third_contact.phone,
            "email": third_contact.email,
            "position": third_contact.position,
            "customer": {
                "id": third_customer.id,
                "form": third_customer.form,
                "name": third_customer.name,
                "inn": third_customer.inn,
                "address": third_customer.address,
                "notes": third_customer.notes,
            },
        },
        {
            "id": fourth_contact.id,
            "first_name": fourth_contact.first_name,
            "last_name": fourth_contact.last_name,
            "father_name": fourth_contact.father_name,
            "phone": fourth_contact.phone,
            "email": fourth_contact.email,
            "position": fourth_contact.position,
            "customer": {
                "id": fouth_customer.id,
                "form": fouth_customer.form,
                "name": fouth_customer.name,
                "inn": fouth_customer.inn,
                "address": fouth_customer.address,
                "notes": fouth_customer.notes,
            },
        },
    ]

    response = client.get(
        "/contacts", params={"customer": [sample_customer.name, another_customer.name]}
    )
    assert response.status_code == 200
    assert response.json() == [
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
