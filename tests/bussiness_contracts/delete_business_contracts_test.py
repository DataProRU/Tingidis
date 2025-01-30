def test_delete_business_contracts(client, sample_business_contract):
    response = client.delete(f"/business-contracts/{sample_business_contract.id}")
    assert response.status_code == 204


def test_unauthenticated_user_cannot_delete_business_contracts(client, sample_business_contract):
    client.headers = {}
    response = client.delete(f"/business-contracts/{sample_business_contract.id}")
    assert response.status_code == 401
