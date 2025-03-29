def test_filters_agreements(
    client,
    sample_agreement,
    another_agreement,
    third_agreement,
    sample_contract,
    another_contract,
):
    response = client.get(
        "/agreements",
        params={"number": [sample_agreement.number, another_agreement.number]},
    )
    assert response.status_code == 200
    assert response.json() == [
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
            "contract": {
                "id": another_contract.id,
                "code": another_contract.code,
                "name": another_contract.name,
                "customer": another_contract.customer,
                "executor": another_contract.executor,
                "number": another_contract.number,
                "sign_date": (
                    another_contract.sign_date.isoformat()
                    if another_contract.sign_date
                    else None
                ),
                "price": float(another_contract.price),
                "theme": another_contract.theme,
                "evolution": another_contract.evolution,
            },
        },
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
            "contract": {
                "id": sample_contract.id,
                "code": sample_contract.code,
                "name": sample_contract.name,
                "customer": sample_contract.customer,
                "executor": sample_contract.executor,
                "number": sample_contract.number,
                "sign_date": (
                    sample_contract.sign_date.isoformat()
                    if sample_contract.sign_date
                    else None
                ),
                "price": float(sample_contract.price),
                "theme": sample_contract.theme,
                "evolution": sample_contract.evolution,
            },
        },
    ]

    # 2. Фильтр по name (строка)
    response = client.get(
        "/agreements", params={"name": [another_agreement.name, third_agreement.name]}
    )
    assert response.status_code == 200
    assert response.json() == [
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
            "contract": {
                "id": sample_contract.id,
                "code": sample_contract.code,
                "name": sample_contract.name,
                "customer": sample_contract.customer,
                "executor": sample_contract.executor,
                "number": sample_contract.number,
                "sign_date": (
                    sample_contract.sign_date.isoformat()
                    if sample_contract.sign_date
                    else None
                ),
                "price": float(sample_contract.price),
                "theme": sample_contract.theme,
                "evolution": sample_contract.evolution,
            },
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
            "contract": {
                "id": sample_contract.id,
                "code": sample_contract.code,
                "name": sample_contract.name,
                "customer": sample_contract.customer,
                "executor": sample_contract.executor,
                "number": sample_contract.number,
                "sign_date": (
                    sample_contract.sign_date.isoformat()
                    if sample_contract.sign_date
                    else None
                ),
                "price": float(sample_contract.price),
                "theme": sample_contract.theme,
                "evolution": sample_contract.evolution,
            },
        },
    ]

    # 3. Фильтр по price (число)
    response = client.get(
        "/agreements",
        params={"price": [another_agreement.price, third_agreement.price]},
    )
    assert response.status_code == 200
    assert response.json() == [
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
            "contract": {
                "id": another_contract.id,
                "code": another_contract.code,
                "name": another_contract.name,
                "customer": another_contract.customer,
                "executor": another_contract.executor,
                "number": another_contract.number,
                "sign_date": (
                    another_contract.sign_date.isoformat()
                    if another_contract.sign_date
                    else None
                ),
                "price": float(another_contract.price),
                "theme": another_contract.theme,
                "evolution": another_contract.evolution,
            },
        },
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
            "contract": {
                "id": sample_contract.id,
                "code": sample_contract.code,
                "name": sample_contract.name,
                "customer": sample_contract.customer,
                "executor": sample_contract.executor,
                "number": sample_contract.number,
                "sign_date": (
                    sample_contract.sign_date.isoformat()
                    if sample_contract.sign_date
                    else None
                ),
                "price": float(sample_contract.price),
                "theme": sample_contract.theme,
                "evolution": sample_contract.evolution,
            },
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
            "contract": {
                "id": sample_contract.id,
                "code": sample_contract.code,
                "name": sample_contract.name,
                "customer": sample_contract.customer,
                "executor": sample_contract.executor,
                "number": sample_contract.number,
                "sign_date": (
                    sample_contract.sign_date.isoformat()
                    if sample_contract.sign_date
                    else None
                ),
                "price": float(sample_contract.price),
                "theme": sample_contract.theme,
                "evolution": sample_contract.evolution,
            },
        },
    ]

    # 4. Фильтр по deadline (дата)
    response = client.get(
        "/agreements",
        params={
            "deadline": [
                sample_agreement.deadline.isoformat(),
                third_agreement.deadline.isoformat(),
            ]
        },
    )
    assert response.status_code == 200
    assert response.json() == [
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
            "contract": {
                "id": another_contract.id,
                "code": another_contract.code,
                "name": another_contract.name,
                "customer": another_contract.customer,
                "executor": another_contract.executor,
                "number": another_contract.number,
                "sign_date": (
                    another_contract.sign_date.isoformat()
                    if another_contract.sign_date
                    else None
                ),
                "price": float(another_contract.price),
                "theme": another_contract.theme,
                "evolution": another_contract.evolution,
            },
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
            "contract": {
                "id": sample_contract.id,
                "code": sample_contract.code,
                "name": sample_contract.name,
                "customer": sample_contract.customer,
                "executor": sample_contract.executor,
                "number": sample_contract.number,
                "sign_date": (
                    sample_contract.sign_date.isoformat()
                    if sample_contract.sign_date
                    else None
                ),
                "price": float(sample_contract.price),
                "theme": sample_contract.theme,
                "evolution": sample_contract.evolution,
            },
        },
    ]

    # 5. Фильтр по contract_name
    response = client.get(
        "/agreements",
        params={"contract_name": [another_contract.name, sample_contract.name]},
    )
    assert response.status_code == 200
    assert response.json() == [
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
            "contract": {
                "id": another_contract.id,
                "code": another_contract.code,
                "name": another_contract.name,
                "customer": another_contract.customer,
                "executor": another_contract.executor,
                "number": another_contract.number,
                "sign_date": (
                    another_contract.sign_date.isoformat()
                    if another_contract.sign_date
                    else None
                ),
                "price": float(another_contract.price),
                "theme": another_contract.theme,
                "evolution": another_contract.evolution,
            },
        },
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
            "contract": {
                "id": sample_contract.id,
                "code": sample_contract.code,
                "name": sample_contract.name,
                "customer": sample_contract.customer,
                "executor": sample_contract.executor,
                "number": sample_contract.number,
                "sign_date": (
                    sample_contract.sign_date.isoformat()
                    if sample_contract.sign_date
                    else None
                ),
                "price": float(sample_contract.price),
                "theme": sample_contract.theme,
                "evolution": sample_contract.evolution,
            },
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
            "contract": {
                "id": sample_contract.id,
                "code": sample_contract.code,
                "name": sample_contract.name,
                "customer": sample_contract.customer,
                "executor": sample_contract.executor,
                "number": sample_contract.number,
                "sign_date": (
                    sample_contract.sign_date.isoformat()
                    if sample_contract.sign_date
                    else None
                ),
                "price": float(sample_contract.price),
                "theme": sample_contract.theme,
                "evolution": sample_contract.evolution,
            },
        },
    ]
