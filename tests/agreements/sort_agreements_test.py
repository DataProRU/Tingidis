from datetime import date

import pytest


@pytest.mark.asyncio
async def test_sort_agreements_asc(
    client, sample_agreement, another_agreement, third_agreement
):
    """
    Тест сортировки соглашений по возрастанию (asc).
    """
    # Сортировка по полю "name" (по возрастанию)
    response = client.get("/agreements", params={"sortBy": "name", "sortDir": "asc"})
    assert response.status_code == 200

    agreements = response.json()
    # Проверяем, что соглашения отсортированы по имени в алфавитном порядке
    assert agreements[0]["name"] == "new_test_agreement"
    assert agreements[1]["name"] == "test_agreement"
    assert agreements[2]["name"] == "third_agreement"


@pytest.mark.asyncio
async def test_sort_agreements_desc(
    client, sample_agreement, another_agreement, third_agreement
):
    """
    Тест сортировки соглашений по убыванию (desc).
    """
    # Сортировка по полю "name" (по убыванию)
    response = client.get("/agreements", params={"sortBy": "name", "sortDir": "desc"})
    assert response.status_code == 200

    agreements = response.json()
    # Проверяем, что соглашения отсортированы по имени в обратном алфавитном порядке
    assert agreements[0]["name"] == "third_agreement"
    assert agreements[1]["name"] == "test_agreement"
    assert agreements[2]["name"] == "new_test_agreement"


@pytest.mark.asyncio
async def test_sort_agreements_by_price_asc(
    client, sample_agreement, another_agreement, third_agreement
):
    """
    Тест сортировки соглашений по полю "price" (по возрастанию).
    """
    # Сортировка по полю "price" (по возрастанию)
    response = client.get("/agreements", params={"sortBy": "price", "sortDir": "asc"})
    assert response.status_code == 200

    agreements = response.json()
    # Проверяем, что соглашения отсортированы по цене в порядке возрастания
    assert agreements[0]["price"] == 1000
    assert agreements[1]["price"] == 1500
    assert agreements[2]["price"] == 2000


@pytest.mark.asyncio
async def test_sort_agreements_by_price_desc(
    client, sample_agreement, another_agreement, third_agreement
):
    """
    Тест сортировки соглашений по полю "price" (по убыванию).
    """
    # Сортировка по полю "price" (по убыванию)
    response = client.get("/agreements", params={"sortBy": "price", "sortDir": "desc"})
    assert response.status_code == 200

    agreements = response.json()
    # Проверяем, что соглашения отсортированы по цене в порядке убывания
    assert agreements[0]["price"] == 2000
    assert agreements[1]["price"] == 1500
    assert agreements[2]["price"] == 1000


@pytest.mark.asyncio
async def test_sort_agreements_by_deadline_asc(
    client, sample_agreement, another_agreement, third_agreement
):
    """
    Тест сортировки соглашений по полю "deadline" (по возрастанию).
    """
    # Сортировка по полю "deadline" (по возрастанию)
    response = client.get(
        "/agreements", params={"sortBy": "deadline", "sortDir": "asc"}
    )
    assert response.status_code == 200

    agreements = response.json()
    # Проверяем, что соглашения отсортированы по дедлайну в порядке возрастания
    assert agreements[0]["deadline"] == date(2024, 1, 1).isoformat()
    assert agreements[1]["deadline"] == date(2024, 2, 2).isoformat()
    assert agreements[2]["deadline"] == date(2025, 3, 3).isoformat()


@pytest.mark.asyncio
async def test_sort_agreements_by_deadline_desc(
    client, sample_agreement, another_agreement, third_agreement
):
    """
    Тест сортировки соглашений по полю "deadline" (по убыванию).
    """
    # Сортировка по полю "deadline" (по убыванию)
    response = client.get(
        "/agreements", params={"sortBy": "deadline", "sortDir": "desc"}
    )
    assert response.status_code == 200

    agreements = response.json()
    # Проверяем, что соглашения отсортированы по дедлайну в порядке убывания
    assert agreements[0]["deadline"] == date(2025, 3, 3).isoformat()
    assert agreements[1]["deadline"] == date(2024, 2, 2).isoformat()
    assert agreements[2]["deadline"] == date(2024, 1, 1).isoformat()


@pytest.mark.asyncio
async def test_sort_agreements_by_number_asc(
    client, sample_agreement, another_agreement, third_agreement
):
    """
    Тест сортировки соглашений по полю "number" (возрастанию).
    """
    response = client.get("/agreements", params={"sortBy": "number", "sortDir": "asc"})
    assert response.status_code == 200

    agreements = response.json()
    assert agreements[0]["number"] == "11111"
    assert agreements[1]["number"] == "1234567890"
    assert agreements[2]["number"] == "987654321"


@pytest.mark.asyncio
async def test_sort_agreements_by_number_desc(
    client, sample_agreement, another_agreement, third_agreement
):
    """
    Тест сортировки соглашений по полю "number" (убывание).
    """
    response = client.get("/agreements", params={"sortBy": "number", "sortDir": "desc"})
    assert response.status_code == 200

    agreements = response.json()
    assert agreements[0]["number"] == "987654321"
    assert agreements[1]["number"] == "1234567890"
    assert agreements[2]["number"] == "11111"


@pytest.mark.asyncio
async def test_sort_agreements_by_notes_asc(
    client, sample_agreement, another_agreement, third_agreement
):
    """
    Тест сортировки соглашений по полю "notes" (возрастание).
    """
    response = client.get("/agreements", params={"sortBy": "notes", "sortDir": "asc"})
    assert response.status_code == 200

    agreements = response.json()
    assert agreements[0]["notes"] == "first notes"
    assert agreements[1]["notes"] == "new_test notes"
    assert agreements[2]["notes"] == "third notes"


@pytest.mark.asyncio
async def test_sort_agreements_by_notes_desc(
    client, sample_agreement, another_agreement, third_agreement
):
    """
    Тест сортировки соглашений по полю "notes" (убывание).
    """
    response = client.get("/agreements", params={"sortBy": "notes", "sortDir": "desc"})
    assert response.status_code == 200

    agreements = response.json()
    assert agreements[0]["notes"] == "third notes"
    assert agreements[1]["notes"] == "new_test notes"
    assert agreements[2]["notes"] == "first notes"


@pytest.mark.asyncio
async def test_sort_agreements_by_contract_asc(
    client, sample_agreement, another_agreement, third_agreement
):
    """
    Тест сортировки соглашений по полю "contract" (возрастание).
    """
    response = client.get(
        "/agreements", params={"sortBy": "contract", "sortDir": "asc"}
    )
    assert response.status_code == 200

    agreements = response.json()
    assert agreements[0]["contract"]["name"] == "fourth_contract_name"
    assert agreements[1]["contract"]["name"] == "new_test_name_1"
    assert agreements[2]["contract"]["name"] == "test_name_2"


@pytest.mark.asyncio
async def test_sort_agreements_by_contract_desc(
    client, sample_agreement, another_agreement, third_agreement
):
    """
    Тест сортировки соглашений по полю "contract" (убывание).
    """
    response = client.get(
        "/agreements", params={"sortBy": "contract", "sortDir": "desc"}
    )
    assert response.status_code == 200

    agreements = response.json()
    assert agreements[0]["contract"]["name"] == "test_name_2"
    assert agreements[1]["contract"]["name"] == "new_test_name_1"
    assert agreements[2]["contract"]["name"] == "fourth_contract_name"
