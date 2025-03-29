def test_filters_contracts(
    client,
    sample_contract,
    another_contract,
    third_contract,
    sample_object,
    another_object,
    third_object,
    sample_customer,
    another_customer,
    third_customer,
    sample_user,
    another_user,
    third_user,
    sample_agreement,
    another_agreement,
    third_agreement,
):
    response = client.get(
        "/contracts", params={"object_code": [sample_object.code, another_object.code]}
    )
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
                    "price": float(another_agreement.price),
                    "deadline": (
                        another_agreement.deadline.isoformat()
                        if another_agreement.deadline
                        else None
                    ),
                    "notes": another_agreement.notes,
                    "contract": another_agreement.contract,
                },
                {
                    "id": third_agreement.id,
                    "name": third_agreement.name,
                    "number": third_agreement.number,
                    "price": float(third_agreement.price),
                    "deadline": (
                        third_agreement.deadline.isoformat()
                        if third_agreement.deadline
                        else None
                    ),
                    "notes": third_agreement.notes,
                    "contract": third_agreement.contract,
                },
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
                    "price": float(sample_agreement.price),
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
        {
            "id": third_contract.id,
            "name": third_contract.name,
            "customer": {
                "id": third_customer.id,
                "form": third_customer.form,
                "name": third_customer.name,
                "address": third_customer.address,
                "inn": third_customer.inn,
                "notes": third_customer.notes,
            },
            "executor": {
                "id": third_user.id,
                "first_name": third_user.first_name,
                "last_name": third_user.last_name,
                "father_name": third_user.father_name,
                "full_name": third_user.full_name,
                "position": third_user.position,
                "phone": third_user.phone,
                "email": third_user.email,
                "telegram": third_user.telegram,
                "birthday": (
                    third_user.birthday.isoformat() if third_user.birthday else None
                ),
                "category": third_user.category,
                "specialization": third_user.specialization,
                "username": third_user.username,
                "notes": third_user.notes,
                "password": None,
                "role": third_user.role,
                "notification": third_user.notification,
            },
            "code": {
                "id": third_object.id,
                "code": third_object.code,
                "name": third_object.name,
                "comment": third_object.comment,
            },
            "number": third_contract.number,
            "sign_date": third_contract.sign_date.isoformat(),
            "price": float(third_contract.price),
            "theme": third_contract.theme,
            "evolution": third_contract.evolution,
            "agreements": [],
        },
    ]

    response = client.get(
        "/contracts", params={"name": [sample_contract.name, third_contract.name]}
    )
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
            "agreements": [
                {
                    "id": another_agreement.id,
                    "name": another_agreement.name,
                    "number": another_agreement.number,
                    "price": float(another_agreement.price),
                    "deadline": (
                        another_agreement.deadline.isoformat()
                        if another_agreement.deadline
                        else None
                    ),
                    "notes": another_agreement.notes,
                    "contract": another_agreement.contract,
                },
                {
                    "id": third_agreement.id,
                    "name": third_agreement.name,
                    "number": third_agreement.number,
                    "price": float(third_agreement.price),
                    "deadline": (
                        third_agreement.deadline.isoformat()
                        if third_agreement.deadline
                        else None
                    ),
                    "notes": third_agreement.notes,
                    "contract": third_agreement.contract,
                },
            ],
            "number": sample_contract.number,
            "sign_date": sample_contract.sign_date.isoformat(),
            "price": float(sample_contract.price),
            "theme": sample_contract.theme,
            "evolution": sample_contract.evolution,
        },
        {
            "id": third_contract.id,
            "name": third_contract.name,
            "customer": {
                "id": third_customer.id,
                "form": third_customer.form,
                "name": third_customer.name,
                "address": third_customer.address,
                "inn": third_customer.inn,
                "notes": third_customer.notes,
            },
            "executor": {
                "id": third_user.id,
                "first_name": third_user.first_name,
                "last_name": third_user.last_name,
                "father_name": third_user.father_name,
                "full_name": third_user.full_name,
                "position": third_user.position,
                "phone": third_user.phone,
                "email": third_user.email,
                "telegram": third_user.telegram,
                "birthday": (
                    third_user.birthday.isoformat() if third_user.birthday else None
                ),
                "category": third_user.category,
                "specialization": third_user.specialization,
                "username": third_user.username,
                "notes": third_user.notes,
                "password": None,
                "role": third_user.role,
                "notification": third_user.notification,
            },
            "code": {
                "id": third_object.id,
                "code": third_object.code,
                "name": third_object.name,
                "comment": third_object.comment,
            },
            "agreements": [],
            "number": third_contract.number,
            "sign_date": third_contract.sign_date.isoformat(),
            "price": float(third_contract.price),
            "theme": third_contract.theme,
            "evolution": third_contract.evolution,
        },
    ]

    response = client.get(
        "/contracts", params={"customer": [another_customer.name, third_customer.name]}
    )
    assert response.status_code == 200
    assert response.json() == [
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
                "password": None,
                "notes": another_user.notes,
                "role": another_user.role,
                "notification": another_user.notification,
            },
            "code": {
                "id": another_object.id,
                "code": another_object.code,
                "name": another_object.name,
                "comment": another_object.comment,
            },
            "agreements": [
                {
                    "id": sample_agreement.id,
                    "name": sample_agreement.name,
                    "number": sample_agreement.number,
                    "price": float(sample_agreement.price),
                    "deadline": (
                        sample_agreement.deadline.isoformat()
                        if sample_agreement.deadline
                        else None
                    ),
                    "notes": sample_agreement.notes,
                    "contract": sample_agreement.contract,
                },
            ],
            "number": another_contract.number,
            "sign_date": another_contract.sign_date.isoformat(),
            "price": float(another_contract.price),
            "theme": another_contract.theme,
            "evolution": another_contract.evolution,
        },
        {
            "id": third_contract.id,
            "name": third_contract.name,
            "customer": {
                "id": third_customer.id,
                "form": third_customer.form,
                "name": third_customer.name,
                "address": third_customer.address,
                "inn": third_customer.inn,
                "notes": third_customer.notes,
            },
            "executor": {
                "id": third_user.id,
                "first_name": third_user.first_name,
                "last_name": third_user.last_name,
                "father_name": third_user.father_name,
                "full_name": third_user.full_name,
                "position": third_user.position,
                "phone": third_user.phone,
                "email": third_user.email,
                "telegram": third_user.telegram,
                "birthday": (
                    third_user.birthday.isoformat() if third_user.birthday else None
                ),
                "category": third_user.category,
                "specialization": third_user.specialization,
                "username": third_user.username,
                "notes": third_user.notes,
                "password": None,
                "role": third_user.role,
                "notification": third_user.notification,
            },
            "code": {
                "id": third_object.id,
                "code": third_object.code,
                "name": third_object.name,
                "comment": third_object.comment,
            },
            "agreements": [],
            "number": third_contract.number,
            "sign_date": third_contract.sign_date.isoformat(),
            "price": float(third_contract.price),
            "theme": third_contract.theme,
            "evolution": third_contract.evolution,
        },
    ]

    response = client.get(
        "/contracts",
        params={"executor": [sample_user.full_name, another_user.full_name]},
    )
    assert response.status_code == 200
    assert response.json() == [
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
                "password": None,
                "notes": another_user.notes,
                "role": another_user.role,
                "notification": another_user.notification,
            },
            "code": {
                "id": another_object.id,
                "code": another_object.code,
                "name": another_object.name,
                "comment": another_object.comment,
            },
            "agreements": [
                {
                    "id": sample_agreement.id,
                    "name": sample_agreement.name,
                    "number": sample_agreement.number,
                    "price": float(sample_agreement.price),
                    "deadline": (
                        sample_agreement.deadline.isoformat()
                        if sample_agreement.deadline
                        else None
                    ),
                    "notes": sample_agreement.notes,
                    "contract": sample_agreement.contract,
                },
            ],
            "number": another_contract.number,
            "sign_date": another_contract.sign_date.isoformat(),
            "price": float(another_contract.price),
            "theme": another_contract.theme,
            "evolution": another_contract.evolution,
        },
    ]

    response = client.get(
        "/contracts",
        params={"number": [sample_contract.number, another_contract.number]},
    )
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
            "agreements": [
                {
                    "id": another_agreement.id,
                    "name": another_agreement.name,
                    "number": another_agreement.number,
                    "price": float(another_agreement.price),
                    "deadline": (
                        another_agreement.deadline.isoformat()
                        if another_agreement.deadline
                        else None
                    ),
                    "notes": another_agreement.notes,
                    "contract": another_agreement.contract,
                },
                {
                    "id": third_agreement.id,
                    "name": third_agreement.name,
                    "number": third_agreement.number,
                    "price": float(third_agreement.price),
                    "deadline": (
                        third_agreement.deadline.isoformat()
                        if third_agreement.deadline
                        else None
                    ),
                    "notes": third_agreement.notes,
                    "contract": third_agreement.contract,
                },
            ],
            "number": sample_contract.number,
            "sign_date": sample_contract.sign_date.isoformat(),
            "price": float(sample_contract.price),
            "theme": sample_contract.theme,
            "evolution": sample_contract.evolution,
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
                "password": None,
                "notes": another_user.notes,
                "role": another_user.role,
                "notification": another_user.notification,
            },
            "code": {
                "id": another_object.id,
                "code": another_object.code,
                "name": another_object.name,
                "comment": another_object.comment,
            },
            "agreements": [
                {
                    "id": sample_agreement.id,
                    "name": sample_agreement.name,
                    "number": sample_agreement.number,
                    "price": float(sample_agreement.price),
                    "deadline": (
                        sample_agreement.deadline.isoformat()
                        if sample_agreement.deadline
                        else None
                    ),
                    "notes": sample_agreement.notes,
                    "contract": sample_agreement.contract,
                },
            ],
            "number": another_contract.number,
            "sign_date": another_contract.sign_date.isoformat(),
            "price": float(another_contract.price),
            "theme": another_contract.theme,
            "evolution": another_contract.evolution,
        },
    ]

    response = client.get(
        "/contracts",
        params={"sign_data": [sample_contract.sign_date, another_contract.sign_date]},
    )
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
            "agreements": [
                {
                    "id": another_agreement.id,
                    "name": another_agreement.name,
                    "number": another_agreement.number,
                    "price": float(another_agreement.price),
                    "deadline": (
                        another_agreement.deadline.isoformat()
                        if another_agreement.deadline
                        else None
                    ),
                    "notes": another_agreement.notes,
                    "contract": another_agreement.contract,
                },
                {
                    "id": third_agreement.id,
                    "name": third_agreement.name,
                    "number": third_agreement.number,
                    "price": float(third_agreement.price),
                    "deadline": (
                        third_agreement.deadline.isoformat()
                        if third_agreement.deadline
                        else None
                    ),
                    "notes": third_agreement.notes,
                    "contract": third_agreement.contract,
                },
            ],
            "number": sample_contract.number,
            "sign_date": sample_contract.sign_date.isoformat(),
            "price": float(sample_contract.price),
            "theme": sample_contract.theme,
            "evolution": sample_contract.evolution,
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
                "password": None,
                "notes": another_user.notes,
                "role": another_user.role,
                "notification": another_user.notification,
            },
            "code": {
                "id": another_object.id,
                "code": another_object.code,
                "name": another_object.name,
                "comment": another_object.comment,
            },
            "agreements": [
                {
                    "id": sample_agreement.id,
                    "name": sample_agreement.name,
                    "number": sample_agreement.number,
                    "price": float(sample_agreement.price),
                    "deadline": (
                        sample_agreement.deadline.isoformat()
                        if sample_agreement.deadline
                        else None
                    ),
                    "notes": sample_agreement.notes,
                    "contract": sample_agreement.contract,
                },
            ],
            "number": another_contract.number,
            "sign_date": another_contract.sign_date.isoformat(),
            "price": float(another_contract.price),
            "theme": another_contract.theme,
            "evolution": another_contract.evolution,
        },
        {
            "id": third_contract.id,
            "name": third_contract.name,
            "customer": {
                "id": third_customer.id,
                "form": third_customer.form,
                "name": third_customer.name,
                "address": third_customer.address,
                "inn": third_customer.inn,
                "notes": third_customer.notes,
            },
            "executor": {
                "id": third_user.id,
                "first_name": third_user.first_name,
                "last_name": third_user.last_name,
                "father_name": third_user.father_name,
                "full_name": third_user.full_name,
                "position": third_user.position,
                "phone": third_user.phone,
                "email": third_user.email,
                "telegram": third_user.telegram,
                "birthday": (
                    third_user.birthday.isoformat() if third_user.birthday else None
                ),
                "category": third_user.category,
                "specialization": third_user.specialization,
                "username": third_user.username,
                "password": None,
                "notes": third_user.notes,
                "role": third_user.role,
                "notification": third_user.notification,
            },
            "code": {
                "id": third_object.id,
                "code": third_object.code,
                "name": third_object.name,
                "comment": third_object.comment,
            },
            "agreements": [],
            "number": third_contract.number,
            "sign_date": third_contract.sign_date.isoformat(),
            "price": float(third_contract.price),
            "theme": third_contract.theme,
            "evolution": third_contract.evolution,
        },
    ]

    response = client.get(
        "/contracts", params={"price": [third_contract.price, another_contract.price]}
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": third_contract.id,
            "name": third_contract.name,
            "customer": {
                "id": third_customer.id,
                "form": third_customer.form,
                "name": third_customer.name,
                "address": third_customer.address,
                "inn": third_customer.inn,
                "notes": third_customer.notes,
            },
            "executor": {
                "id": third_user.id,
                "first_name": third_user.first_name,
                "last_name": third_user.last_name,
                "father_name": third_user.father_name,
                "full_name": third_user.full_name,
                "position": third_user.position,
                "phone": third_user.phone,
                "email": third_user.email,
                "telegram": third_user.telegram,
                "birthday": (
                    third_user.birthday.isoformat() if third_user.birthday else None
                ),
                "category": third_user.category,
                "specialization": third_user.specialization,
                "username": third_user.username,
                "password": None,
                "notes": third_user.notes,
                "role": third_user.role,
                "notification": third_user.notification,
            },
            "code": {
                "id": third_object.id,
                "code": third_object.code,
                "name": third_object.name,
                "comment": third_object.comment,
            },
            "agreements": [],
            "number": third_contract.number,
            "sign_date": third_contract.sign_date.isoformat(),
            "price": float(third_contract.price),
            "theme": third_contract.theme,
            "evolution": third_contract.evolution,
        },
    ]

    response = client.get(
        "/contracts", params={"theme": [sample_contract.theme, another_contract.theme]}
    )
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
            "agreements": [
                {
                    "id": another_agreement.id,
                    "name": another_agreement.name,
                    "number": another_agreement.number,
                    "price": float(another_agreement.price),
                    "deadline": (
                        another_agreement.deadline.isoformat()
                        if another_agreement.deadline
                        else None
                    ),
                    "notes": another_agreement.notes,
                    "contract": another_agreement.contract,
                },
                {
                    "id": third_agreement.id,
                    "name": third_agreement.name,
                    "number": third_agreement.number,
                    "price": float(third_agreement.price),
                    "deadline": (
                        third_agreement.deadline.isoformat()
                        if third_agreement.deadline
                        else None
                    ),
                    "notes": third_agreement.notes,
                    "contract": third_agreement.contract,
                },
            ],
            "number": sample_contract.number,
            "sign_date": sample_contract.sign_date.isoformat(),
            "price": float(sample_contract.price),
            "theme": sample_contract.theme,
            "evolution": sample_contract.evolution,
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
                "password": None,
                "notes": another_user.notes,
                "role": another_user.role,
                "notification": another_user.notification,
            },
            "code": {
                "id": another_object.id,
                "code": another_object.code,
                "name": another_object.name,
                "comment": another_object.comment,
            },
            "agreements": [
                {
                    "id": sample_agreement.id,
                    "name": sample_agreement.name,
                    "number": sample_agreement.number,
                    "price": float(sample_agreement.price),
                    "deadline": (
                        sample_agreement.deadline.isoformat()
                        if sample_agreement.deadline
                        else None
                    ),
                    "notes": sample_agreement.notes,
                    "contract": sample_agreement.contract,
                },
            ],
            "number": another_contract.number,
            "sign_date": another_contract.sign_date.isoformat(),
            "price": float(another_contract.price),
            "theme": another_contract.theme,
            "evolution": another_contract.evolution,
        },
    ]

    response = client.get(
        "/contracts",
        params={"evolution": [sample_contract.evolution, another_contract.evolution]},
    )
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
            "agreements": [
                {
                    "id": another_agreement.id,
                    "name": another_agreement.name,
                    "number": another_agreement.number,
                    "price": float(another_agreement.price),
                    "deadline": (
                        another_agreement.deadline.isoformat()
                        if another_agreement.deadline
                        else None
                    ),
                    "notes": another_agreement.notes,
                    "contract": another_agreement.contract,
                },
                {
                    "id": third_agreement.id,
                    "name": third_agreement.name,
                    "number": third_agreement.number,
                    "price": float(third_agreement.price),
                    "deadline": (
                        third_agreement.deadline.isoformat()
                        if third_agreement.deadline
                        else None
                    ),
                    "notes": third_agreement.notes,
                    "contract": third_agreement.contract,
                },
            ],
            "number": sample_contract.number,
            "sign_date": sample_contract.sign_date.isoformat(),
            "price": float(sample_contract.price),
            "theme": sample_contract.theme,
            "evolution": sample_contract.evolution,
        },
        {
            "id": third_contract.id,
            "name": third_contract.name,
            "customer": {
                "id": third_customer.id,
                "form": third_customer.form,
                "name": third_customer.name,
                "address": third_customer.address,
                "inn": third_customer.inn,
                "notes": third_customer.notes,
            },
            "executor": {
                "id": third_user.id,
                "first_name": third_user.first_name,
                "last_name": third_user.last_name,
                "father_name": third_user.father_name,
                "full_name": third_user.full_name,
                "position": third_user.position,
                "phone": third_user.phone,
                "email": third_user.email,
                "telegram": third_user.telegram,
                "birthday": (
                    third_user.birthday.isoformat() if third_user.birthday else None
                ),
                "category": third_user.category,
                "specialization": third_user.specialization,
                "username": third_user.username,
                "password": None,
                "notes": third_user.notes,
                "role": third_user.role,
                "notification": third_user.notification,
            },
            "code": {
                "id": third_object.id,
                "code": third_object.code,
                "name": third_object.name,
                "comment": third_object.comment,
            },
            "agreements": [],
            "number": third_contract.number,
            "sign_date": third_contract.sign_date.isoformat(),
            "price": float(third_contract.price),
            "theme": third_contract.theme,
            "evolution": third_contract.evolution,
        },
    ]
