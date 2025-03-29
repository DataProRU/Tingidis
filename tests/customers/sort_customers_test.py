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
    assert customers[0]["name"] == another_customer.name  # "test_name"
    assert customers[1]["name"] == sample_customer.name  # "new_test_name"
    assert customers[2]["name"] == third_customer.name  # "third_customer"


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
    assert customers[0]["name"] == third_customer.name  # "third_customer"
    assert customers[1]["name"] == sample_customer.name  # "new_test_name"
    assert customers[2]["name"] == another_customer.name  # "test_name"


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
    assert customers[0]["address"] == "another test addres"  # Alex
    assert customers[1]["address"] == "second"  # Nicolas
    assert customers[2]["address"] == "second"  # John
    assert customers[3]["address"] == "test addres"  # Ivan


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
    assert customers[0]["inn"] == "111111"  # Ivan
    assert customers[1]["inn"] == "22222"  # Alex
    assert customers[2]["inn"] == "new test inn"  # Nicolas
    assert customers[3]["inn"] == "test inn"  # John


@pytest.mark.asyncio
async def test_sort_customers_by_form_of_ownership_asc(
    client,
    sample_customer,
    another_customer,
    third_customer,
    fouth_customer,
    sample_form,
    another_form,
    third_form,
    foth_form,
):
    """
    Тест сортировки клиентов по форме собственности (form_of_ownership) в порядке возрастания.
    """
    response = client.get(
        "/customers",
        params={
            "form": [sample_form.name, another_form.name],
            "sortBy": "name",
            "sortDir": "asc",
        },
    )
    assert response.status_code == 200

    customers = response.json()
    # Проверяем, что клиенты отсортированы по форме собственности в алфавитном порядке
    assert customers[0]["form"]["name"] == another_form.name
    assert customers[1]["form"]["name"] == sample_form.name
