def test_delete_objects(client, sample_object):
    object = sample_object
    response = client.delete(f"/objects/{object.id}")
    assert response.status_code == 204


def test_unauthenticated_user_cannot_delete_object(client, sample_object):
    client.headers = {}
    object = sample_object
    response = client.delete(f"/objects/{object.id}")
    assert response.status_code == 401
