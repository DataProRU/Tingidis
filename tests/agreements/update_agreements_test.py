def test_update_agreement(client, another_contract, sample_agreement):
    contract_id = another_contract.id
    agreement = sample_agreement
    agreement_payload = {
        "name": "test_agreement",
        "number": "1234567890",
        "price": 1000,
        "deadline": "2001-02-02",
        "notes": "test notes",
        "contract": contract_id,
    }
    response = client.patch(f"/agreements/{agreement.id}", json=agreement_payload)
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "test_agreement"
    assert result["number"] == "1234567890"
    assert result["price"] == 1000
    assert result["deadline"] == "2001-02-02"
    assert result["notes"] == "test notes"
    assert result["contract"] == {
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
    }


def test_unauthenticated_user_cannot_update_agreement(
    client, another_contract, sample_agreement
):
    client.headers = {}
    contract_id = another_contract.id
    agreement = sample_agreement
    agreement_payload = {
        "name": "test_agreement",
        "number": "1234567890",
        "price": 1000,
        "deadline": "2001-02-02",
        "notes": "test notes",
        "contract": contract_id,
    }
    response = client.patch(f"/users/{agreement.id}", json=agreement_payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
