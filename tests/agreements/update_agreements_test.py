def test_update_agreement(client, another_business_contract, sample_agreement):
    contract_id = another_business_contract.id
    agreement = sample_agreement
    agreement_payload = {
        "name": "test_agreement",
        "number": "1234567890",
        "deadline": "2001-02-02",
        "notes": "test notes",
        "contract": contract_id,
    }
    response = client.patch(f"/agreements/{agreement.id}", json=agreement_payload)
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "test_agreement"
    assert result["number"] == "1234567890"
    assert result["deadline"] == "2001-02-02"
    assert result["notes"] == "test notes"
    assert result["contract"] == contract_id


def test_unauthenticated_user_cannot_update_agreement(
    client, another_business_contract, sample_agreement
):
    client.headers = {}
    contract_id = another_business_contract.id
    agreement = sample_agreement
    agreement_payload = {
        "name": "test_agreement",
        "number": "1234567890",
        "deadline": "2001-02-02",
        "notes": "test notes",
        "contract": contract_id,
    }
    response = client.patch(f"/users/{agreement.id}", json=agreement_payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
