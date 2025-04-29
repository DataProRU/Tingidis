import pytest


@pytest.mark.asyncio
async def test_sort_contacts_by_first_name_asc(
    client, sample_contact, another_contact, third_contact
):
    """
    Тест сортировки контактов по имени (first_name) в порядке возрастания.
    """
    response = client.get(
        "/contacts", params={"sortBy": "first_name", "sortDir": "asc"}
    )
    assert response.status_code == 200

    contacts = response.json()
    # Проверяем, что контакты отсортированы по имени в алфавитном порядке
    assert contacts[0]["first_name"] == "Alex"
    assert contacts[1]["first_name"] == "Ivan"
    assert contacts[2]["first_name"] == "Maria"


@pytest.mark.asyncio
async def test_sort_contacts_by_first_name_desc(
    client, sample_contact, another_contact, third_contact
):
    """
    Тест сортировки контактов по имени (first_name) в порядке убывания.
    """
    response = client.get(
        "/contacts", params={"sortBy": "first_name", "sortDir": "desc"}
    )
    assert response.status_code == 200

    contacts = response.json()
    # Проверяем, что контакты отсортированы по имени в обратном алфавитном порядке
    assert contacts[0]["first_name"] == "Maria"
    assert contacts[1]["first_name"] == "Ivan"
    assert contacts[2]["first_name"] == "Alex"


@pytest.mark.asyncio
async def test_sort_contacts_by_last_name_asc(
    client, sample_contact, another_contact, third_contact
):
    """
    Тест сортировки контактов по фамилии (last_name) в порядке возрастания.
    """
    response = client.get("/contacts", params={"sortBy": "last_name", "sortDir": "asc"})
    assert response.status_code == 200

    contacts = response.json()
    # Проверяем, что контакты отсортированы по фамилии в алфавитном порядке
    assert contacts[0]["last_name"] == "Alexeev"
    assert contacts[1]["last_name"] == "Ivanov"
    assert contacts[2]["last_name"] == "Sidorova"


@pytest.mark.asyncio
async def test_sort_contacts_by_last_name_desc(
    client, sample_contact, another_contact, third_contact
):
    """
    Тест сортировки контактов по фамилии (last_name) в порядке возрастания.
    """
    response = client.get("/contacts", params={"sortBy": "last_name", "sortDir": "desc"})
    assert response.status_code == 200

    contacts = response.json()
    # Проверяем, что контакты отсортированы по фамилии в алфавитном порядке
    assert contacts[0]["last_name"] == "Sidorova"
    assert contacts[1]["last_name"] == "Ivanov"
    assert contacts[2]["last_name"] == "Alexeev"


@pytest.mark.asyncio
async def test_sort_contacts_by_father_name_asc(
    client, sample_contact, another_contact, third_contact
):
    """
    Тест сортировки контактов по отчеству (father_name) в порядке возрастания.
    """
    response = client.get("/contacts", params={"sortBy": "father_name", "sortDir": "asc"})
    assert response.status_code == 200

    contacts = response.json()
    assert contacts[0]["father_name"] == "Alexeevich"
    assert contacts[1]["father_name"] == "Ivanovich"
    assert contacts[2]["father_name"] == "Petrovna"


@pytest.mark.asyncio
async def test_sort_contacts_by_father_name_desc(
    client, sample_contact, another_contact, third_contact
):
    """
    Тест сортировки контактов по отчеству (father_name) в порядке убывания.
    """
    response = client.get("/contacts", params={"sortBy": "father_name", "sortDir": "desc"})
    assert response.status_code == 200

    contacts = response.json()
    assert contacts[0]["father_name"] == "Petrovna"
    assert contacts[1]["father_name"] == "Ivanovich"
    assert contacts[2]["father_name"] == "Alexeevich"


@pytest.mark.asyncio
async def test_sort_contacts_by_email_asc(
    client, sample_contact, another_contact, third_contact
):
    """
    Тест сортировки контактов по почте (email) в порядке возрастания.
    """
    response = client.get("/contacts", params={"sortBy": "email", "sortDir": "asc"})
    assert response.status_code == 200

    contacts = response.json()
    assert contacts[0]["email"] == "aled@mail.com"
    assert contacts[1]["email"] == "ivanov@mail.com"
    assert contacts[2]["email"] == "maria@example.com"


@pytest.mark.asyncio
async def test_sort_contacts_by_email_desc(
    client, sample_contact, another_contact, third_contact
):
    """
    Тест сортировки контактов по почте (email) в порядке убывания.
    """
    response = client.get("/contacts", params={"sortBy": "email", "sortDir": "desc"})
    assert response.status_code == 200

    contacts = response.json()
    assert contacts[0]["email"] == "maria@example.com"
    assert contacts[1]["email"] == "ivanov@mail.com"
    assert contacts[2]["email"] == "aled@mail.com"


@pytest.mark.asyncio
async def test_sort_contacts_by_phone_asc(
    client, sample_contact, another_contact, third_contact
):
    """
    Тест сортировки контактов по почте (phone) в порядке возрастания.
    """
    response = client.get("/contacts", params={"sortBy": "phone", "sortDir": "asc"})
    assert response.status_code == 200

    contacts = response.json()
    assert contacts[0]["phone"] == "+70000000000"
    assert contacts[1]["phone"] == "+70000000001"
    assert contacts[2]["phone"] == "+79112345678"


@pytest.mark.asyncio
async def test_sort_contacts_by_phone_desc(
    client, sample_contact, another_contact, third_contact
):
    """
    Тест сортировки контактов по почте (phone) в порядке убывания.
    """
    response = client.get("/contacts", params={"sortBy": "phone", "sortDir": "desc"})
    assert response.status_code == 200

    contacts = response.json()
    assert contacts[0]["phone"] == "+79112345678"
    assert contacts[1]["phone"] == "+70000000001"
    assert contacts[2]["phone"] == "+70000000000"


@pytest.mark.asyncio
async def test_sort_contacts_by_position_asc(
    client, sample_contact, another_contact, third_contact
):
    """
    Тест сортировки контактов по должности (position) в порядке возрастанию.
    """
    response = client.get("/contacts", params={"sortBy": "position", "sortDir": "asc"})
    assert response.status_code == 200

    contacts = response.json()
    assert contacts[0]["position"] == "engineer"
    assert contacts[1]["position"] == "manager"
    assert contacts[2]["position"] == "worker"


@pytest.mark.asyncio
async def test_sort_contacts_by_position_desc(
    client, sample_contact, another_contact, third_contact
):
    """
    Тест сортировки контактов по должности (position) в порядке убывания.
    """
    response = client.get("/contacts", params={"sortBy": "position", "sortDir": "desc"})
    assert response.status_code == 200

    contacts = response.json()
    assert contacts[0]["position"] == "worker"
    assert contacts[1]["position"] == "manager"
    assert contacts[2]["position"] == "engineer"


@pytest.mark.asyncio
async def test_sort_contacts_by_customer_asc(
    client, sample_contact, another_contact, third_contact
):
    """
    Тест сортировки контактов по должности (customer) в порядке возрастанию.
    """
    response = client.get("/contacts", params={"sortBy": "customer", "sortDir": "asc"})
    assert response.status_code == 200

    contacts = response.json()
    assert contacts[0]["customer"]["name"] == "Alex"
    assert contacts[1]["customer"]["name"] == "Ivan"
    assert contacts[2]["customer"]["name"] == "Nicolas"


@pytest.mark.asyncio
async def test_sort_contacts_by_customer_desc(
    client, sample_contact, another_contact, third_contact
):
    """
    Тест сортировки контактов по должности (customer) в порядке убывания.
    """
    response = client.get("/contacts", params={"sortBy": "customer", "sortDir": "desc"})
    assert response.status_code == 200

    contacts = response.json()
    assert contacts[0]["customer"]["name"] == "Nicolas"
    assert contacts[1]["customer"]["name"] == "Ivan"
    assert contacts[2]["customer"]["name"] == "Alex"
