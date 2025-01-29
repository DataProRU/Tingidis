def test_delete_personal_contract(client, sample_person_contract):
    response = client.delete(f"/person-contracts/{sample_person_contract.id}")
    assert response.status_code == 204


def test_unauthenticated_user_cannot_delete_object(client, sample_person_contract):
    client.headers = {}
    response = client.delete(f"/person-contracts/{sample_person_contract.id}")
    assert response.status_code == 401
