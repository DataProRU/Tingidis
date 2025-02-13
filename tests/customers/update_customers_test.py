def test_update_customer(client, sample_customer, another_form):
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
    result = response.json()
    assert result["name"] == "new Ivan"
    assert result["form"] == {"id": another_form.id, "name": another_form.name}
    assert result["address"] == "new test addres"
    assert result["inn"] == "new test inn"
    assert result["notes"] == "other note"


def test_unauthenticated_user_cannot_update_customer(
    client, sample_customer, another_form
):
    object = sample_customer
    client.headers = {}
    payload = {
        "name": "new Ivan",
        "form": another_form.id,
        "address": "new test addres",
        "inn": "new test inn",
        "notes": "other note",
    }
    response = client.patch(f"/customers/{object.id}", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
