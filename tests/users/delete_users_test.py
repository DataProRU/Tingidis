def test_delete_user(client, sample_user):
    user = sample_user
    response = client.delete(f"/users/{user.id}")
    assert response.status_code == 204


def test_unauthenticated_user_cannot_delete_user(client, sample_user):
    client.headers = {}
    user = sample_user
    response = client.delete(f"/users/{user.id}")
    assert response.status_code == 401
