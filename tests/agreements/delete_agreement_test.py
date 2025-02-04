def test_delete_sample_agreement(client, sample_agreement):
    agreement = sample_agreement
    response = client.delete(f"/agreements/{agreement.id}")
    assert response.status_code == 204


def test_unauthenticated_user_cannot_delete_user(client, sample_agreement):
    client.headers = {}
    agreement = sample_agreement
    response = client.delete(f"/agreements/{agreement.id}")
    assert response.status_code == 401
