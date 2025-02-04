def test_update_form(client, sample_form):
    object = sample_form
    payload = {"name": "newtest object"}
    response = client.patch(f"/form-of-ownership/{object.id}", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "newtest object"


def test_unauthenticated_user_cannot_update_form(client, sample_form):
    form = sample_form
    client.headers = {}
    payload = {"name": "newtest object"}
    response = client.patch(f"/form-of-ownership/{form.id}", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
