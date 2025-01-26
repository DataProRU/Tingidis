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
    form_1 = sample_form
    form_2 = another_form
    response = client.get("/form-of-ownership")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": form_1.id,
            "name": form_1.name,
        },
        {
            "id": form_2.id,
            "name": form_2.name,
        },
    ]


def test_get_form(client, sample_form):
    form = sample_form
    response = client.get(f"/form-of-ownership/{form.id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": form.id,
        "name": form.name,
    }


def test_unauthenticated_user_cannot_read_fomrs(client, sample_form):
    client.headers = {}
    object = sample_form
    response = client.get(f"/form-of-ownership/{object.id}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
