def test_update_object(client, sample_object):
    object = sample_object
    payload = {"code": "123458", "name": "newtest object", "comment": "new comment"}
    response = client.patch(f"/objects/{object.id}", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["code"] == "123458"
    assert result["name"] == "newtest object"
    assert result["comment"] == "new comment"


def test_unauthenticated_user_cannot_update_object(client, sample_object):
    object = sample_object
    client.headers = {}
    payload = {"code": "123458", "name": "newtest object", "comment": "new comment"}
    response = client.patch(f"/objects/{object.id}", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
