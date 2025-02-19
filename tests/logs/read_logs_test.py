def test_get_empty_logs(client):
    response = client.get("/logs")
    assert response.status_code == 200
    assert response.json() == []


def test_unauthenticated_user_cannot_read_logs(client):
    client.headers = {}
    response = client.get("/logs")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_read_logs(
    client, sample_customer, another_form, sample_agreement, sample_user
):
    payload = {"name": "test form"}
    response = client.post("/form-of-ownership", json=payload)
    assert response.status_code == 201

    customer = sample_customer
    payload = {
        "name": "new Ivan",
        "form": another_form.id,
        "address": "new test addres",
        "inn": "new test inn",
        "notes": "other note",
    }
    response = client.patch(f"/customers/{customer.id}", json=payload)
    assert response.status_code == 200

    agreement = sample_agreement
    response = client.delete(f"/agreements/{agreement.id}")
    assert response.status_code == 204

    response = client.get("/logs")
    assert response.status_code == 200
    result = response.json()
    assert "Создание формы собственности" in result[2]["action"]
    assert result[2]["datetime"] is not None
    assert result[2]["user"] == sample_user.username

    assert result[1]["action"] == f"Обновление заказчика (ID: {sample_customer.id})"
    assert result[1]["datetime"] is not None
    assert result[1]["user"] == sample_user.username

    assert result[0]["action"] == f"Удаление соглашения (ID: {sample_agreement.id})"
    assert result[0]["datetime"] is not None
    assert result[0]["user"] == sample_user.username
