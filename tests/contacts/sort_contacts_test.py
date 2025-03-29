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
    assert contacts[0]["first_name"] == another_contact.first_name  # Alex
    assert contacts[1]["first_name"] == sample_contact.first_name  # Ivan
    assert contacts[2]["first_name"] == third_contact.first_name  # Maria


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
    assert contacts[0]["first_name"] == third_contact.first_name  # Maria
    assert contacts[1]["first_name"] == sample_contact.first_name  # Ivan
    assert contacts[2]["first_name"] == another_contact.first_name  # Alex


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
    assert contacts[0]["last_name"] == another_contact.last_name  # Alexeev
    assert contacts[1]["last_name"] == sample_contact.last_name  # Ivanov
    assert contacts[2]["last_name"] == third_contact.last_name  # Sidorova


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
    # Проверяем, что контакты отсортированы по должности в обратном алфавитном порядке
    assert contacts[0]["position"] == "worker"  #  "worker"
    assert contacts[1]["position"] == "manager"  #  "manager"
    assert contacts[2]["position"] == "engineer"  # "engineer"
