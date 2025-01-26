def test_delete_user(client, sample_user):
    user = sample_user
    response = client.delete(f"/users/{user.id}")
    assert response.status_code == 403
    assert response.json() == {"detail": "Отсутствует доступ к запросу"}


def test_delete_user_by_admin(admin_client, sample_user):
    user = sample_user
    response = admin_client.delete(f"/users/{user.id}")
    assert response.status_code == 204


def test_unauthenticated_user_cannot_delete_user(client, sample_user):
    client.headers = {}
    user = sample_user
    response = client.delete(f"/users/{user.id}")
    assert response.status_code == 401
