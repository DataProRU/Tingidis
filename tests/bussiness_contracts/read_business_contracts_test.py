from decimal import Decimal

def test_get_empty_business_contracts(client):
    response = client.get("/business-contracts")
    assert response.status_code == 200
    assert response.json() == []


def test_unauthenticated_user_cannot_read_business_contracts(client):
    client.headers = {}
    response = client.get("/business-contracts")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_get_agreements(client, sample_business_contract, another_business_contract):
    response = client.get("/business-contracts")
    assert response.status_code == 200

    # Убедитесь, что объекты в правильном порядке
    contracts = sorted([sample_business_contract, another_business_contract], key=lambda x: x.code)

    expected_result = [
        {
            "id": contract.id,
            "code": contract.code,
            "name": contract.name,
            "customer": contract.customer,
            "executor": contract.executor,
            "number": contract.number,
            "sign_date": str(contract.sign_date),
            "price": float(contract.price) if isinstance(contract.price, Decimal) else contract.price,
            "theme": contract.theme,
            "evolution": contract.evolution
        } for contract in contracts
    ]

    assert response.json() == expected_result


def test_get_business_contract(client, sample_business_contract):
    response = client.get("/business-contracts")
    assert response.status_code == 200

    expected_response = [
        {
            "id": sample_business_contract.id,
            "code": sample_business_contract.code,
            "name": sample_business_contract.name,
            "customer": sample_business_contract.customer,
            "executor": sample_business_contract.executor,
            "number": sample_business_contract.number,
            "sign_date": str(sample_business_contract.sign_date),
            "price": float(sample_business_contract.price) if isinstance(sample_business_contract.price, Decimal) else sample_business_contract.price,
            "theme": sample_business_contract.theme,
            "evolution": sample_business_contract.evolution
    }
    ]

    assert response.json() == expected_response


