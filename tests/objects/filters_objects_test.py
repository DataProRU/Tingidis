def test_filters_objects(client, sample_object, another_object):
    response = client.get(
        "/objects", params={"code": [sample_object.code, another_object.code]}
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": sample_object.id,
            "code": sample_object.code,
            "name": sample_object.name,
            "comment": sample_object.comment,
        },
        {
            "id": another_object.id,
            "code": another_object.code,
            "name": another_object.name,
            "comment": another_object.comment,
        },
    ]

    response = client.get(
        "/objects", params={"name": [sample_object.name, another_object.name]}
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": sample_object.id,
            "code": sample_object.code,
            "name": sample_object.name,
            "comment": sample_object.comment,
        },
        {
            "id": another_object.id,
            "code": another_object.code,
            "name": another_object.name,
            "comment": another_object.comment,
        },
    ]

    response = client.get(
        "/objects", params={"comment": [sample_object.comment, another_object.comment]}
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": sample_object.id,
            "code": sample_object.code,
            "name": sample_object.name,
            "comment": sample_object.comment,
        },
        {
            "id": another_object.id,
            "code": another_object.code,
            "name": another_object.name,
            "comment": another_object.comment,
        },
    ]
