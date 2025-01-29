def test_get_empty_person_contracts(client):
    response = client.get("/person-contracts")
    assert response.status_code == 200
    assert response.json() == []


def test_unauthenticated_user_cannot_read_person_contracts(client):
    client.headers = {}
    response = client.get("/person-contracts")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}


# Пример теста с использованием мока
def test_get_personal_contracts(
    client, sample_person_contract, another_person_contract
):
    response = client.get(f"/person-contracts/")
    assert response.status_code == 200
    expected_result = [
        {
            "id": sample_person_contract.id,
            "first_name": sample_person_contract.first_name,
            "last_name": sample_person_contract.last_name,
            "father_name": sample_person_contract.father_name,
            "email": sample_person_contract.email,
            "position": sample_person_contract.position,
            "customer": 1,
        },
        {
            "id": another_person_contract.id,
            "first_name": another_person_contract.first_name,
            "last_name": another_person_contract.last_name,
            "father_name": another_person_contract.father_name,
            "email": another_person_contract.email,
            "position": another_person_contract.position,
            "customer": 2,
        },
    ]
    assert response.json() == expected_result


def test_get_person_contract(client, sample_person_contract):
    response = client.get(f"/person-contracts/{sample_person_contract.id}")
    assert response.status_code == 200
    expected_result = {
        "id": sample_person_contract.id,
        "first_name": sample_person_contract.first_name,
        "last_name": sample_person_contract.last_name,
        "father_name": sample_person_contract.father_name,
        "email": sample_person_contract.email,
        "position": sample_person_contract.position,
        "customer": 1,
    }
    assert response.json() == expected_result
