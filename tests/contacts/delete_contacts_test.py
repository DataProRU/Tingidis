def test_delete_contact(client, sample_contact):
    response = client.delete(f"/contacts/{sample_contact.id}")
    assert response.status_code == 204


def test_unauthenticated_user_cannot_delete_contact(client, sample_contact):
    client.headers = {}
    response = client.delete(f"/contacts/{sample_contact.id}")
    assert response.status_code == 401
