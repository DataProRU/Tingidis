def test_delete_customers(client, sample_customer):
    customer = sample_customer
    response = client.delete(f"/customers/{customer.id}")
    assert response.status_code == 204


def test_unauthenticated_user_cannot_delete_customer(client, sample_customer):
    client.headers = {}
    customer = sample_customer
    response = client.delete(f"/customers/{customer.id}")
    assert response.status_code == 401
