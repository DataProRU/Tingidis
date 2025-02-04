def test_delete_form(client, sample_form):
    form = sample_form
    response = client.delete(f"/form-of-ownership/{form.id}")
    assert response.status_code == 204


def test_unauthenticated_user_cannot_delete_form(client, sample_object):
    client.headers = {}
    object = sample_object
    response = client.delete(f"/form-of-ownership/{object.id}")
    assert response.status_code == 401
