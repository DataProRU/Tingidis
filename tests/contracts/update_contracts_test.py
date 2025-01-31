async def test_update_contract(
    sample_contract, client, sample_object, sample_customer, sample_user
):
    payload = {
        "code": sample_object.id,
        "name": "test contract name",
        "customer": sample_customer.id,
        "executor": sample_user.id,
        "number": "123456",
        "sign_date": "2025-02-11",
        "price": 2000.21,
        "theme": "test",
        "evolution": "test evolution",
    }

    response = client.patch(f"/contracts/{sample_contract.id}", json=payload)
    assert response.status_code == 200

    result = response.json()

    assert result["name"] == "test contract name"

    # Проверяем customer как объект
    assert result["customer"]["id"] == sample_customer.id
    assert result["customer"]["name"] == sample_customer.name
    assert result["customer"]["address"] == sample_customer.address
    assert result["customer"]["inn"] == sample_customer.inn
    assert "form" in result["customer"]  # Новое поле

    # Проверяем executor как объект
    assert result["executor"]["id"] == sample_user.id
    assert result["executor"]["username"] == sample_user.username
    assert result["executor"]["role"] == sample_user.role
    assert "first_name" in result["executor"]  # Новое поле
    assert "last_name" in result["executor"]  # Новое поле

    assert result["code"]["id"] == sample_object.id
    assert result["code"]["code"] == sample_object.code  # Добавлено
    assert result["code"]["name"] == sample_object.name  # Добавлено
    assert "comment" in result["code"]  # Новое поле

    assert result["number"] == "123456"
    assert result["sign_date"] == "2025-02-11"
    assert result["price"] == 2000.21
    assert result["theme"] == "test"
    assert result["evolution"] == "test evolution"


def test_unauthenticated_user_cannot_update_contract(
    client, sample_object, sample_customer, sample_user, sample_contract
):

    client.headers = {}
    payload = {
        "code": sample_object.id,
        "name": "test contract name",
        "customer": sample_customer.id,
        "executor": sample_user.id,
        "number": "123456",
        "sign_date": "2025-02-11",
        "price": 2000.21,
        "theme": "test",
        "evolution": "test evolution",
    }
    response = client.patch(f"/contracts/{sample_contract.id}", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
