def test_delete_contracts(client, sample_contract):
    response = client.delete(f"/contracts/{sample_contract.id}")
    assert response.status_code == 204


def test_unauthenticated_user_cannot_delete_contracts(client, sample_contract):
    client.headers = {}
    response = client.delete(f"/contracts/{sample_contract.id}")
    assert response.status_code == 401
