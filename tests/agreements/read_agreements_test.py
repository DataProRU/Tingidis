def test_get_empty_agreements(client):
    response = client.get("/agreements")
    assert response.status_code == 200
    assert response.json() == []


def test_unauthenticated_user_cannot_read_agreements(client):
    client.headers = {}
    response = client.get("/agreements")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_get_agreements(client, sample_agreement, another_agreement):
    response = client.get("/agreements")
    assert response.status_code == 200

    assert response.json() == [
        {
            "id": sample_agreement.id,
            "name": sample_agreement.name,
            "number": sample_agreement.number,
            "deadline": (
                sample_agreement.deadline.isoformat()
                if sample_agreement.deadline
                else None
            ),
            "notes": sample_agreement.notes,
            "contract": 1,
        },
        {
            "id": another_agreement.id,
            "name": another_agreement.name,
            "number": another_agreement.number,
            "deadline": (
                another_agreement.deadline.isoformat()
                if another_agreement.deadline
                else None
            ),
            "notes": another_agreement.notes,
            "contract": 2,
        },
    ]


def test_get_agreement(client, sample_agreement):
    agreement = sample_agreement
    response = client.get(f"/agreements/{agreement.id}")
    assert response.status_code == 200

    expected_response = {
        "id": agreement.id,
        "name": agreement.name,
        "number": agreement.number,
        "deadline": (
            agreement.deadline.isoformat() if agreement.deadline else None
        ),  # Convert date to string
        "notes": agreement.notes,
        "contract": agreement.contract,
    }

    assert response.json() == expected_response
