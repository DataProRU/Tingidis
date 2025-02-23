def test_get_empty_contracts(client):
    response = client.get("/contracts")
    assert response.status_code == 200
    assert response.json() == []


def test_unauthenticated_user_cannot_read_contracts(client):
    client.headers = {}
    response = client.get("/contracts")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_get_contracts(
    client,
    sample_contract,
    another_contract,
    sample_user,
    another_user,
    sample_customer,
    another_customer,
    sample_object,
    another_object,
    sample_agreement,
    another_agreement,
):

    response = client.get("/contracts")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": sample_contract.id,
            "name": sample_contract.name,
            "customer": {
                "id": sample_customer.id,
                "form": sample_customer.form,
                "name": sample_customer.name,
                "address": sample_customer.address,
                "inn": sample_customer.inn,
                "notes": sample_customer.notes,
            },
            "executor": {
                "id": sample_user.id,
                "first_name": sample_user.first_name,
                "last_name": sample_user.last_name,
                "father_name": sample_user.father_name,
                "full_name": sample_user.full_name,
                "position": sample_user.position,
                "phone": sample_user.phone,
                "email": sample_user.email,
                "telegram": sample_user.telegram,
                "birthday": (
                    sample_user.birthday.isoformat() if sample_user.birthday else None
                ),
                "category": sample_user.category,
                "specialization": sample_user.specialization,
                "username": sample_user.username,
                "password": None,
                "notes": sample_user.notes,
                "role": sample_user.role,
                "notification": sample_user.notification,
            },
            "code": {
                "id": sample_object.id,
                "code": sample_object.code,
                "name": sample_object.name,
                "comment": sample_object.comment,
            },
            "number": sample_contract.number,
            "sign_date": sample_contract.sign_date.isoformat(),
            "price": float(sample_contract.price),
            "theme": sample_contract.theme,
            "evolution": sample_contract.evolution,
            "agreements": [
                {
                    "id": another_agreement.id,
                    "name": another_agreement.name,
                    "number": another_agreement.number,
                    "price": another_agreement.price,
                    "deadline": (
                        another_agreement.deadline.isoformat()
                        if another_agreement.deadline
                        else None
                    ),
                    "notes": another_agreement.notes,
                    "contract": another_agreement.contract,
                }
            ],
        },
        {
            "id": another_contract.id,
            "name": another_contract.name,
            "customer": {
                "id": another_customer.id,
                "form": another_customer.form,
                "name": another_customer.name,
                "address": another_customer.address,
                "inn": another_customer.inn,
                "notes": another_customer.notes,
            },
            "executor": {
                "id": another_user.id,
                "first_name": another_user.first_name,
                "last_name": another_user.last_name,
                "father_name": another_user.father_name,
                "full_name": another_user.full_name,
                "position": another_user.position,
                "phone": another_user.phone,
                "email": another_user.email,
                "telegram": another_user.telegram,
                "birthday": (
                    another_user.birthday.isoformat() if another_user.birthday else None
                ),
                "category": another_user.category,
                "specialization": another_user.specialization,
                "username": another_user.username,
                "notes": another_user.notes,
                "password": None,
                "role": another_user.role,
                "notification": another_user.notification,
            },
            "code": {
                "id": another_object.id,
                "code": another_object.code,
                "name": another_object.name,
                "comment": another_object.comment,
            },
            "number": another_contract.number,
            "sign_date": another_contract.sign_date.isoformat(),
            "price": float(another_contract.price),
            "theme": another_contract.theme,
            "evolution": another_contract.evolution,
            "agreements": [
                {
                    "id": sample_agreement.id,
                    "name": sample_agreement.name,
                    "number": sample_agreement.number,
                    "price": sample_agreement.price,
                    "deadline": (
                        sample_agreement.deadline.isoformat()
                        if sample_agreement.deadline
                        else None
                    ),
                    "notes": sample_agreement.notes,
                    "contract": sample_agreement.contract,
                }
            ],
        },
    ]


def test_get_contract(
    client,
    sample_contract,
    sample_customer,
    sample_user,
    sample_object,
    another_agreement,
):
    response = client.get(f"/contracts/{sample_contract.id}")
    assert response.status_code == 200

    # Если API возвращает один объект (dict)
    expected_response = {
        "id": sample_contract.id,
        "name": sample_contract.name,
        "customer": {
            "id": sample_customer.id,
            "form": sample_customer.form,
            "name": sample_customer.name,
            "address": sample_customer.address,
            "inn": sample_customer.inn,
            "notes": sample_customer.notes,
        },
        "executor": {
            "id": sample_user.id,
            "first_name": sample_user.first_name,
            "last_name": sample_user.last_name,
            "father_name": sample_user.father_name,
            "full_name": sample_user.full_name,
            "position": sample_user.position,
            "phone": sample_user.phone,
            "email": sample_user.email,
            "telegram": sample_user.telegram,
            "birthday": (
                sample_user.birthday.isoformat() if sample_user.birthday else None
            ),
            "category": sample_user.category,
            "specialization": sample_user.specialization,
            "username": sample_user.username,
            "password": None,
            "notes": sample_user.notes,
            "role": sample_user.role,
            "notification": None,
        },
        "code": {
            "id": sample_object.id,
            "code": sample_object.code,
            "name": sample_object.name,
            "comment": sample_object.comment,
        },
        "number": sample_contract.number,
        "sign_date": sample_contract.sign_date.isoformat(),
        "price": float(sample_contract.price),
        "theme": sample_contract.theme,
        "evolution": sample_contract.evolution,
        "agreements": [
            {
                "id": another_agreement.id,
                "name": another_agreement.name,
                "number": another_agreement.number,
                "price": another_agreement.price,
                "deadline": (
                    another_agreement.deadline.isoformat()
                    if another_agreement.deadline
                    else None
                ),
                "notes": another_agreement.notes,
                "contract": another_agreement.contract,
            }
        ],
    }

    assert response.json() == expected_response


def test_unauthenticated_user_cannot_read_contract(client, sample_contract):
    client.headers = {}
    response = client.get(f"/contracts/{sample_contract.id}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
