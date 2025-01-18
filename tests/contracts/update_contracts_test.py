from datetime import datetime


def test_update_contract(client, sample_contract, sample_object):
    payload = {
        "code": sample_object.id,
        "name": "Sample Contract",
        "number": "1234567890",
        "sign_date": datetime(2024, 2, 2).date().isoformat(),
        "price": 2000.21,
        "theme": "Sample Theme",
        "evolution": "Sample Evolution",
    }
    response = client.patch(f"/contracts/{sample_contract.id}", json=payload)
    assert response.status_code == 200


def test_unauthenticated_user_cannot_update_contract(
    client, sample_contract, sample_object
):
    client.headers = {}
    payload = {
        "code": sample_object.id,
        "name": "Sample Contract",
        "number": "1234567890",
        "sign_date": datetime(2024, 2, 2).date().isoformat(),
        "price": 2000.21,
        "theme": "Sample Theme",
        "evolution": "Sample Evolution",
    }
    response = client.patch(f"/contracts/{sample_contract.id}", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
