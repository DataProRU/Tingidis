def test_get_empty_objects(client):
    response = client.get("/objects")
    assert response.status_code == 200
    assert response.json() == []


def test_unauthenticated_user_cannot_read_objects(client):
    client.headers = {}
    response = client.get("/objects")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_get_objects(client, sample_object, another_object):
    object_1 = sample_object
    object_2 = another_object
    response = client.get("/objects")
    assert response.status_code == 200
    expected_result = [
        {
            "code": object_1.code,
            "comment": object_1.comment,
            "id": object_1.id,
            "name": object_1.name,
        },
        {
            "code": object_2.code,
            "comment": object_2.comment,
            "id": object_2.id,
            "name": object_2.name,
        },
    ]
    assert response.json() == expected_result


def test_get_object(client, sample_object):
    object = sample_object
    response = client.get(f"/objects/{object.id}")
    assert response.status_code == 200
    assert response.json() == {
        "code": object.code,
        "comment": object.comment,
        "id": object.id,
        "name": object.name,
    }


def test_unauthenticated_user_cannot_read_object(client, sample_object):
    client.headers = {}
    object = sample_object
    response = client.get(f"/objects/{object.id}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
