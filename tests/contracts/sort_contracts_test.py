from datetime import date

import pytest


@pytest.mark.asyncio
async def test_sort_contract_by_name_asc(
    client, sample_contract, another_contract, third_contract
):
    """
    Тест сортировки соглашений по имени (name) в порядке возрастания.
    """
    response = client.get("/contracts", params={"sortBy": "name", "sortDir": "asc"})
    assert response.status_code == 200

    agreements = response.json()
    # Проверяем, что соглашения отсортированы по имени в алфавитном порядке
    assert agreements[0]["name"] == "new_test_name_1"
    assert agreements[1]["name"] == "test_name_2"
    assert agreements[2]["name"] == "third_contract_name"


@pytest.mark.asyncio
async def test_sort_contracts_by_name_desc(
    client, sample_contract, another_contract, third_contract
):
    """
    Тест сортировки соглашений по имени (name) в порядке убывания.
    """
    response = client.get("/contracts", params={"sortBy": "name", "sortDir": "desc"})
    assert response.status_code == 200

    agreements = response.json()
    # Проверяем, что соглашения отсортированы по имени в обратном алфавитном порядке
    assert agreements[0]["name"] == "third_contract_name"
    assert agreements[1]["name"] == "test_name_2"
    assert agreements[2]["name"] == "new_test_name_1"


@pytest.mark.asyncio
async def test_sort_contracts_by_price_asc(
    client, sample_contract, another_contract, third_contract
):
    """
    Тест сортировки соглашений по цене (price) в порядке возрастания.
    """
    response = client.get("/contracts", params={"sortBy": "price", "sortDir": "asc"})
    assert response.status_code == 200

    agreements = response.json()
    # Проверяем, что соглашения отсортированы по цене в порядке возрастания
    assert agreements[0]["price"] == 100.21
    assert agreements[1]["price"] == 2000.21
    assert agreements[2]["price"] == 5000.50


@pytest.mark.asyncio
async def test_sort_contracts_by_price_desc(
    client, sample_contract, another_contract, third_contract
):
    """
    Тест сортировки соглашений по цене (price) в порядке убывания.
    """
    response = client.get("/contracts", params={"sortBy": "price", "sortDir": "desc"})
    assert response.status_code == 200

    agreements = response.json()
    # Проверяем, что соглашения отсортированы по цене в порядке убывания
    assert agreements[0]["price"] == 5000.50
    assert agreements[1]["price"] == 2000.21
    assert agreements[2]["price"] == 100.21


@pytest.mark.asyncio
async def test_sort_contracts_by_sign_date_asc(
    client, sample_contract, another_contract, third_contract
):
    """
    Тест сортировки соглашений по (sign_date) в порядке возрастания.
    """
    response = client.get(
        "/contracts", params={"sortBy": "sign_date", "sortDir": "asc"}
    )
    assert response.status_code == 200

    agreements = response.json()
    assert agreements[0]["sign_date"] == date(2024, 1, 1).isoformat()
    assert agreements[1]["sign_date"] == date(2024, 2, 2).isoformat()
    assert agreements[2]["sign_date"] == date(2024, 3, 3).isoformat()


@pytest.mark.asyncio
async def test_sort_contracts_by_sign_date_desc(
    client, sample_contract, another_contract, third_contract
):
    """
    Тест сортировки соглашений по (sign_date) в порядке убывания.
    """
    response = client.get(
        "/contracts", params={"sortBy": "sign_date", "sortDir": "desc"}
    )
    assert response.status_code == 200

    agreements = response.json()
    assert agreements[0]["sign_date"] == date(2024, 3, 3).isoformat()
    assert agreements[1]["sign_date"] == date(2024, 2, 2).isoformat()
    assert agreements[2]["sign_date"] == date(2024, 1, 1).isoformat()


@pytest.mark.asyncio
async def test_sort_contracts_by_theme_asc(
    client, sample_contract, another_contract, third_contract
):
    """
    Тест сортировки соглашений по дедлайну (theme) в порядке возрастания.
    """
    response = client.get("/contracts", params={"sortBy": "theme", "sortDir": "asc"})
    assert response.status_code == 200

    agreements = response.json()
    assert agreements[0]["theme"] == "test_theme_1"
    assert agreements[1]["theme"] == "test_theme_2"
    assert agreements[2]["theme"] == "third_theme"


@pytest.mark.asyncio
async def test_sort_contracts_by_theme_desc(
    client, sample_contract, another_contract, third_contract
):
    """
    Тест сортировки соглашений по theme в порядке убывания.
    """
    response = client.get("/contracts", params={"sortBy": "theme", "sortDir": "desc"})
    assert response.status_code == 200

    agreements = response.json()
    assert agreements[0]["theme"] == "third_theme"
    assert agreements[1]["theme"] == "test_theme_2"
    assert agreements[2]["theme"] == "test_theme_1"


@pytest.mark.asyncio
async def test_sort_contracts_by_evolution_asc(
    client, sample_contract, another_contract, third_contract
):
    """
    Тест сортировки соглашений по (evolution) в порядке возрастания.
    """
    response = client.get(
        "/contracts", params={"sortBy": "evolution", "sortDir": "asc"}
    )
    assert response.status_code == 200

    agreements = response.json()
    assert agreements[0]["evolution"] == "1. 24.01.2025 13:00:01"
    assert agreements[1]["evolution"] == "2. 24.01.2025 13:00:01"
    assert agreements[2]["evolution"] == "Updated on 2024-03-03"


@pytest.mark.asyncio
async def test_sort_contracts_by_evolution_desc(
    client, sample_contract, another_contract, third_contract
):
    """
    Тест сортировки соглашений по evolution в порядке убывания.
    """
    response = client.get(
        "/contracts", params={"sortBy": "evolution", "sortDir": "desc"}
    )
    assert response.status_code == 200

    agreements = response.json()
    assert agreements[0]["evolution"] == "Updated on 2024-03-03"
    assert agreements[1]["evolution"] == "2. 24.01.2025 13:00:01"
    assert agreements[2]["evolution"] == "1. 24.01.2025 13:00:01"


@pytest.mark.asyncio
async def test_sort_contracts_by_code_asc(
    client, sample_contract, another_contract, third_contract
):
    """
    Тест сортировки соглашений по (code) в порядке возрастания.
    """
    response = client.get("/contracts", params={"sortBy": "code", "sortDir": "asc"})
    assert response.status_code == 200

    agreements = response.json()
    assert agreements[0]["code"]["code"] == "123456"
    assert agreements[1]["code"]["code"] == "123457"
    assert agreements[2]["code"]["code"] == "345678"


@pytest.mark.asyncio
async def test_sort_contracts_by_code_desc(
    client, sample_contract, another_contract, third_contract
):
    """
    Тест сортировки соглашений по code в порядке убывания.
    """
    response = client.get("/contracts", params={"sortBy": "code", "sortDir": "desc"})
    assert response.status_code == 200

    agreements = response.json()
    assert agreements[0]["code"]["code"] == "345678"
    assert agreements[1]["code"]["code"] == "123457"
    assert agreements[2]["code"]["code"] == "123456"


@pytest.mark.asyncio
async def test_sort_contracts_by_number_asc(
    client, sample_contract, another_contract, third_contract
):
    """
    Тест сортировки соглашений по (number) в порядке возрастания.
    """
    response = client.get("/contracts", params={"sortBy": "number", "sortDir": "asc"})
    assert response.status_code == 200

    agreements = response.json()
    assert agreements[0]["number"] == "123456"
    assert agreements[1]["number"] == "654321"
    assert agreements[2]["number"] == "987654"


@pytest.mark.asyncio
async def test_sort_contracts_by_number_desc(
    client, sample_contract, another_contract, third_contract
):
    """
    Тест сортировки соглашений по number в порядке убывания.
    """
    response = client.get("/contracts", params={"sortBy": "number", "sortDir": "desc"})
    assert response.status_code == 200

    agreements = response.json()
    assert agreements[0]["number"] == "987654"
    assert agreements[1]["number"] == "654321"
    assert agreements[2]["number"] == "123456"


@pytest.mark.asyncio
async def test_sort_contracts_by_customer_asc(
    client, sample_contract, another_contract, third_contract
):
    """
    Тест сортировки соглашений по (customer) в порядке возрастания.
    """
    response = client.get("/contracts", params={"sortBy": "customer", "sortDir": "asc"})
    assert response.status_code == 200

    agreements = response.json()
    assert agreements[0]["customer"]["name"] == "Alex"
    assert agreements[1]["customer"]["name"] == "Ivan"
    assert agreements[2]["customer"]["name"] == "Nicolas"


@pytest.mark.asyncio
async def test_sort_contracts_by_customer_desc(
    client, sample_contract, another_contract, third_contract
):
    """
    Тест сортировки соглашений по code в порядке убывания.
    """
    response = client.get(
        "/contracts", params={"sortBy": "customer", "sortDir": "desc"}
    )
    assert response.status_code == 200

    agreements = response.json()
    assert agreements[0]["customer"]["name"] == "Nicolas"
    assert agreements[1]["customer"]["name"] == "Ivan"
    assert agreements[2]["customer"]["name"] == "Alex"


@pytest.mark.asyncio
async def test_sort_contracts_by_executor_asc(
    client, sample_contract, another_contract, third_contract
):
    """
    Тест сортировки соглашений по (executor) в порядке возрастания.
    """
    response = client.get("/contracts", params={"sortBy": "executor", "sortDir": "asc"})
    assert response.status_code == 200

    agreements = response.json()
    assert agreements[0]["executor"]["first_name"] == "Alex"
    assert agreements[1]["executor"]["first_name"] == "Ivan"
    assert agreements[2]["executor"]["first_name"] == "Maria"


@pytest.mark.asyncio
async def test_sort_contracts_by_executor_desc(
    client, sample_contract, another_contract, third_contract
):
    """
    Тест сортировки соглашений по executor в порядке убывания.
    """
    response = client.get(
        "/contracts", params={"sortBy": "executor", "sortDir": "desc"}
    )
    assert response.status_code == 200

    agreements = response.json()
    assert agreements[0]["executor"]["first_name"] == "Maria"
    assert agreements[1]["executor"]["first_name"] == "Ivan"
    assert agreements[2]["executor"]["first_name"] == "Alex"
