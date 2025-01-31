def test_create_agreement(client, sample_contract):
    contract_id = sample_contract.id

    agreement_payload = {
        "name": "test_agreement",
        "number": "1234567890",
        "price": 1000,
        "deadline": "2001-02-02",
        "notes": "test notes",
        "contract": contract_id,
    }
    response = client.post("/agreements", json=agreement_payload)
    assert response.status_code == 201

    result = response.json()
    assert result["name"] == "test_agreement"
    assert result["number"] == "1234567890"
    assert result["deadline"] == "2001-02-02"
    assert result["price"] == 1000
    assert result["notes"] == "test notes"
    assert result["contract"] == contract_id


def test_unauthenticated_user_cannot_create_agreement(client, sample_contract):
    client.headers = {}
    contract_id = sample_contract.id
    agreement_payload = {
        "name": "test_agreement",
        "number": "1234567890",
        "price": 1000,
        "deadline": "2001-02-02",
        "notes": "test notes",
        "contract": contract_id,
    }
    response = client.post("/agreements", json=agreement_payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_cannot_create_agreement_with_empty_field(client):
    payload = {
        "name": "test_agreement",
    }
    response = client.post("/agreements", json=payload)
    assert response.status_code == 422
