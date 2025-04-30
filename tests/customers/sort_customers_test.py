import pytest


@pytest.mark.asyncio
async def test_sort_customers_by_name_asc(
    client, sample_customer, another_customer, third_customer
):
    """
    Тест сортировки клиентов по имени (name) в порядке возрастания.
    """
    response = client.get("/customers", params={"sortBy": "name", "sortDir": "asc"})
    assert response.status_code == 200

    customers = response.json()
    # Проверяем, что клиенты отсортированы по имени в алфавитном порядке
    assert customers[0]["name"] == "Alex"
    assert customers[1]["name"] == "Ivan"
    assert customers[2]["name"] == "Nicolas"


@pytest.mark.asyncio
async def test_sort_customers_by_name_desc(
    client, sample_customer, another_customer, third_customer
):
    """
    Тест сортировки клиентов по имени (name) в порядке убывания.
    """
    response = client.get("/customers", params={"sortBy": "name", "sortDir": "desc"})
    assert response.status_code == 200

    customers = response.json()
    # Проверяем, что клиенты отсортированы по имени в обратном алфавитном порядке
    assert customers[0]["name"] == "Nicolas"
    assert customers[1]["name"] == "Ivan"
    assert customers[2]["name"] == "Alex"


@pytest.mark.asyncio
async def test_sort_customers_by_address_asc(
    client, sample_customer, another_customer, third_customer, fouth_customer
):
    """
    Тест сортировки клиентов по адресу (address) в порядке возрастания.
    """
    response = client.get("/customers", params={"sortBy": "address", "sortDir": "asc"})
    assert response.status_code == 200

    customers = response.json()
    # Проверяем, что клиенты отсортированы по адресу в алфавитном порядке
    assert customers[0]["address"] == "another test addres"
    assert customers[1]["address"] == "second"
    assert customers[2]["address"] == "second"
    assert customers[3]["address"] == "test addres"


@pytest.mark.asyncio
async def test_sort_customers_by_address_desc(
    client, sample_customer, another_customer, third_customer, fouth_customer
):
    """
    Тест сортировки клиентов по адресу (address) в порядке убыванию.
    """
    response = client.get("/customers", params={"sortBy": "address", "sortDir": "desc"})
    assert response.status_code == 200

    customers = response.json()
    # Проверяем, что клиенты отсортированы по адресу в алфавитном порядке
    assert customers[0]["address"] == "test addres"
    assert customers[1]["address"] == "second"
    assert customers[2]["address"] == "second"
    assert customers[3]["address"] == "another test addres"


@pytest.mark.asyncio
async def test_sort_customers_by_inn_asc(
    client, sample_customer, another_customer, third_customer, fouth_customer
):
    """
    Тест сортировки клиентов по ИНН (inn) в порядке возрастания.
    """
    response = client.get("/customers", params={"sortBy": "inn", "sortDir": "asc"})
    assert response.status_code == 200

    customers = response.json()
    # Проверяем, что клиенты отсортированы по ИНН в числовом порядке
    assert customers[0]["inn"] == "111111"
    assert customers[1]["inn"] == "22222"
    assert customers[2]["inn"] == "new test inn"
    assert customers[3]["inn"] == "test inn"


@pytest.mark.asyncio
async def test_sort_customers_by_inn_desc(
    client, sample_customer, another_customer, third_customer, fouth_customer
):
    """
    Тест сортировки клиентов по ИНН (inn) в порядке убыванию.
    """
    response = client.get("/customers", params={"sortBy": "inn", "sortDir": "desc"})
    assert response.status_code == 200

    customers = response.json()
    # Проверяем, что клиенты отсортированы по ИНН в числовом порядке
    assert customers[0]["inn"] == "test inn"
    assert customers[1]["inn"] == "new test inn"
    assert customers[2]["inn"] == "22222"
    assert customers[3]["inn"] == "111111"


@pytest.mark.asyncio
async def test_sort_customers_by_notes_asc(
    client, sample_customer, another_customer, third_customer
):
    """
    Тест сортировки клиентов по (notes) в порядке возрастания.
    """
    response = client.get("/customers", params={"sortBy": "notes", "sortDir": "asc"})
    assert response.status_code == 200

    customers = response.json()
    assert customers[0]["notes"] == "aaa"
    assert customers[1]["notes"] == "Test notes 1"
    assert customers[2]["notes"] == "Test notes 2"


@pytest.mark.asyncio
async def test_sort_customers_by_notes_desc(
    client, sample_customer, another_customer, third_customer
):
    """
    Тест сортировки клиентов по notes в порядке убыванию.
    """
    response = client.get("/customers", params={"sortBy": "notes", "sortDir": "desc"})
    assert response.status_code == 200

    customers = response.json()
    assert customers[0]["notes"] == "Test notes 2"
    assert customers[1]["notes"] == "Test notes 1"
    assert customers[2]["notes"] == "aaa"


@pytest.mark.asyncio
async def test_sort_customers_by_form_asc(
    client, sample_customer, another_customer, third_customer
):
    """
    Тест сортировки клиентов по (form) в порядке возрастания.
    """
    response = client.get("/customers", params={"sortBy": "form", "sortDir": "asc"})
    assert response.status_code == 200

    customers = response.json()
    assert customers[0]["form"]["name"] == "test name"
    assert customers[1]["form"]["name"] == "test name 2"
    assert customers[2]["form"]["name"] == "ИП"


@pytest.mark.asyncio
async def test_sort_customers_by_form_desc(
    client, sample_customer, another_customer, third_customer
):
    """
    Тест сортировки клиентов по form в порядке убыванию.
    """
    response = client.get("/customers", params={"sortBy": "form", "sortDir": "desc"})
    assert response.status_code == 200

    customers = response.json()
    assert customers[0]["form"]["name"] == "ИП"
    assert customers[1]["form"]["name"] == "test name 2"
    assert customers[2]["form"]["name"] == "test name"
