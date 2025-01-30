def test_create_business_contracts(client, sample_object, sample_customer, sample_user):
    payload = {
        "code": str(sample_object.id),
        "name": "test contract name",
        "customer": str(sample_customer.id),
        "executor": str(sample_user.id),
        "number" : "123456",
        "sign_date": "2001-02-01",
        "price" : "2000.21",
        "theme":"test",
        "evolution":"test evolution"
    }
    response = client.post("/business-contracts", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["code"] == sample_object.id
    assert result["name"] == "test contract name"
    assert result["customer"] == sample_customer.id
    assert result["executor"] == sample_user.id
    assert result["number"] == "123456"
    assert result["sign_date"] == "2001-02-01"
    assert result["price"] == 2000.21
    assert result["theme"] == "test"
    assert result["evolution"] == "test evolution"



def test_unauthenticated_user_cannot_create_business_contracts(client, sample_object, sample_customer, sample_user):
    client.headers = {}
    payload = {
        "code": str(sample_object.id),
        "name": "test contract name",
        "customer": str(sample_customer.id),
        "executor": str(sample_user.id),
        "number": "123456",
        "sign_date": "2001-02-01",
        "price": "2000.21",
        "theme": "test",
        "evolution": "test evolution"
    }
    response = client.post("/business-contracts", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_cannot_create_business_contracts_with_empty_field(client, sample_object,):
    payload = {
        "code": str(sample_object.id),
    }
    response = client.post("/business-contracts", json=payload)
    assert response.status_code == 422
