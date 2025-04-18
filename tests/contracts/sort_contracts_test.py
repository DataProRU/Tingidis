import pytest


@pytest.mark.asyncio
async def test_sort_agreements_by_name_asc(
    client, sample_agreement, another_agreement, third_agreement
):
    """
    Тест сортировки соглашений по имени (name) в порядке возрастания.
    """
    response = client.get("/agreements", params={"sortBy": "name", "sortDir": "asc"})
    assert response.status_code == 200

    agreements = response.json()
    # Проверяем, что соглашения отсортированы по имени в алфавитном порядке
    assert agreements[0]["name"] == another_agreement.name  # "new_test_agreement"
    assert agreements[1]["name"] == sample_agreement.name  # "test_agreement"
    assert agreements[2]["name"] == third_agreement.name  # "third_agreement"


@pytest.mark.asyncio
async def test_sort_agreements_by_name_desc(
    client, sample_agreement, another_agreement, third_agreement
):
    """
    Тест сортировки соглашений по имени (name) в порядке убывания.
    """
    response = client.get("/agreements", params={"sortBy": "name", "sortDir": "desc"})
    assert response.status_code == 200

    agreements = response.json()
    # Проверяем, что соглашения отсортированы по имени в обратном алфавитном порядке
    assert agreements[0]["name"] == third_agreement.name  # "third_agreement"
    assert agreements[1]["name"] == sample_agreement.name  # "test_agreement"
    assert agreements[2]["name"] == another_agreement.name  # "new_test_agreement"


@pytest.mark.asyncio
async def test_sort_agreements_by_price_asc(
    client, sample_agreement, another_agreement, third_agreement
):
    """
    Тест сортировки соглашений по цене (price) в порядке возрастания.
    """
    response = client.get("/agreements", params={"sortBy": "price", "sortDir": "asc"})
    assert response.status_code == 200

    agreements = response.json()
    # Проверяем, что соглашения отсортированы по цене в порядке возрастания
    assert agreements[0]["price"] == float(sample_agreement.price)  # 1000.0
    assert agreements[1]["price"] == float(another_agreement.price)  # 1500.0
    assert agreements[2]["price"] == float(third_agreement.price)  # 2000.0


@pytest.mark.asyncio
async def test_sort_agreements_by_price_desc(
    client, sample_agreement, another_agreement, third_agreement
):
    """
    Тест сортировки соглашений по цене (price) в порядке убывания.
    """
    response = client.get("/agreements", params={"sortBy": "price", "sortDir": "desc"})
    assert response.status_code == 200

    agreements = response.json()
    # Проверяем, что соглашения отсортированы по цене в порядке убывания
    assert agreements[0]["price"] == float(third_agreement.price)  # 2000.0
    assert agreements[1]["price"] == float(another_agreement.price)  # 1000.0
    assert agreements[2]["price"] == float(sample_agreement.price)  # 1000.0


@pytest.mark.asyncio
async def test_sort_agreements_by_deadline_asc(
    client, sample_agreement, another_agreement, third_agreement
):
    """
    Тест сортировки соглашений по дедлайну (deadline) в порядке возрастания.
    """
    response = client.get(
        "/agreements", params={"sortBy": "deadline", "sortDir": "asc"}
    )
    assert response.status_code == 200

    agreements = response.json()
    # Проверяем, что соглашения отсортированы по дедлайну в порядке возрастания
    assert (
        agreements[0]["deadline"] == sample_agreement.deadline.isoformat()
    )  # 2024-01-01
    assert (
        agreements[1]["deadline"] == another_agreement.deadline.isoformat()
    )  # 2024-02-02
    assert (
        agreements[2]["deadline"] == third_agreement.deadline.isoformat()
    )  # 2025-03-03


@pytest.mark.asyncio
async def test_sort_agreements_by_deadline_desc(
    client, sample_agreement, another_agreement, third_agreement
):
    """
    Тест сортировки соглашений по дедлайну (deadline) в порядке убывания.
    """
    response = client.get(
        "/agreements", params={"sortBy": "deadline", "sortDir": "desc"}
    )
    assert response.status_code == 200

    agreements = response.json()
    # Проверяем, что соглашения отсортированы по дедлайну в порядке убывания
    assert (
        agreements[0]["deadline"] == third_agreement.deadline.isoformat()
    )  # 2025-03-03
    assert (
        agreements[1]["deadline"] == another_agreement.deadline.isoformat()
    )  # 2024-02-02
    assert (
        agreements[2]["deadline"] == sample_agreement.deadline.isoformat()
    )  # 2024-01-01
