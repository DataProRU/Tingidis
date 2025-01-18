from decimal import Decimal
from datetime import datetime


def test_get_empty_contracts(client):
    response = client.get("/contracts/")
    assert response.status_code == 200
    assert response.json() == []


def test_unauthenticated_user_cannot_read_contracts(client):
    client.headers = {}
    response = client.get("/contracts")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


def test_get_contract(client, sample_contract):
    contract = sample_contract
    response = client.get(f"/contracts/{contract.id}")

    assert response.status_code == 200

    # Преобразуем данные из JSON-ответа к ожидаемым типам
    response_data = response.json()
    response_data["price"] = Decimal(str(response_data["price"]))
    response_data["sign_date"] = datetime.fromisoformat(response_data["sign_date"])

    assert response_data == {
        "id": contract.id,
        "code": contract.code,
        "name": contract.name,
        "number": contract.number,
        "sign_date": datetime(2024, 1, 1, 0, 0),
        "price": Decimal("2000.21"),
        "theme": contract.theme,
        "evolution": contract.evolution,
    }


def test_get_contracts(client, sample_contract, another_contract):
    response = client.get("/contracts")
    assert response.status_code == 200

    contract = sample_contract
    another = another_contract

    assert response.json() == [
        {
            "id": contract.id,
            "code": contract.code,
            "name": contract.name,
            "number": contract.number,
            "sign_date": datetime(2024, 1, 1)
            .date()
            .isoformat(),  # Преобразуем datetime в date и затем в строку
            "price": float(Decimal("2000.21")),  # Преобразуем Decimal в float
            "theme": contract.theme,
            "evolution": contract.evolution,
        },
        {
            "id": another.id,
            "code": another.code,
            "name": another.name,
            "number": another.number,
            "sign_date": datetime(2024, 2, 2)
            .date()
            .isoformat(),  # Преобразуем datetime в date и затем в строку
            "price": float(Decimal("100.21")),  # Преобразуем Decimal в float
            "theme": contract.theme,
            "evolution": contract.evolution,
        },
    ]


def test_unauthenticated_user_cannot_read_contract(client, sample_contract):
    client.headers = {}
    response = client.get(f"/contracts/{sample_contract.id}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
