def test_get_empty_agreements(client):
    response = client.get("/agreements")
    assert response.status_code == 200
    assert response.json() == []


def test_unauthenticated_user_cannot_read_agreements(client):
    client.headers = {}
    response = client.get("/agreements")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_get_agreements(
    client, sample_agreement, another_agreement, sample_contract, another_contract
):
    response = client.get("/agreements")
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


def test_get_agreement(client, sample_agreement, another_contract):
    agreement = sample_agreement
    response = client.get(f"/agreements/{agreement.id}")
    assert response.status_code == 200

    expected_response = {
        "id": agreement.id,
        "name": agreement.name,
        "number": agreement.number,
        "price": agreement.price,
        "deadline": (agreement.deadline.isoformat() if agreement.deadline else None),
        "notes": agreement.notes,
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
    }

    assert response.json() == expected_response


def test_unauthenticated_user_cannot_read_agreement(client, sample_agreement):
    client.headers = {}
    response = client.get(f"/agreements/{sample_agreement.id}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
