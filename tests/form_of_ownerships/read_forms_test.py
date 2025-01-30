def test_get_empty_forms(client):
    response = client.get("/form-of-ownership")
    assert response.status_code == 200
    assert response.json() == []


def test_unauthenticated_user_cannot_read_forms(client):
    client.headers = {}
    response = client.get("/form-of-ownership")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_get_forms(client, sample_form, another_form):
    response = client.get("/form-of-ownership")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": sample_form.id,
            "name": sample_form.name,
        },
        {
            "id": another_form.id,
            "name": another_form.name,
        },
    ]


def test_get_form(client, sample_form):
    response = client.get(f"/form-of-ownership/{sample_form.id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": sample_form.id,
        "name": sample_form.name,
    }


def test_unauthenticated_user_cannot_read_form(client, sample_form):
    client.headers = {}
    response = client.get(f"/form-of-ownership/{sample_form.id}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
