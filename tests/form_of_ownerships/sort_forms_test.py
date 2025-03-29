import pytest


@pytest.mark.asyncio
async def test_sort_form_of_ownerships_by_name_asc(
    client, third_form, foth_form, fifth_form
):
    """
    Тест сортировки форм собственности по имени в порядке возрастания.
    """
    response = client.get(
        "/form-of-ownership", params={"sortBy": "name", "sortDir": "asc"}
    )
    assert response.status_code == 200

    forms = response.json()
    assert len(forms) >= 3
    assert forms[0]["name"] == "ЗАО"
    assert forms[1]["name"] == "ИП"
    assert forms[2]["name"] == "ОАО"


@pytest.mark.asyncio
async def test_sort_form_of_ownerships_by_name_desc(
    client, third_form, foth_form, fifth_form
):
    """
    Тест сортировки форм собственности по имени в порядке убывания.
    """
    response = client.get(
        "/form-of-ownership", params={"sortBy": "name", "sortDir": "desc"}
    )
    assert response.status_code == 200

    forms = response.json()
    assert len(forms) >= 3
    assert forms[0]["name"] == "ОАО"
    assert forms[1]["name"] == "ИП"
    assert forms[2]["name"] == "ЗАО"


@pytest.mark.asyncio
async def test_sort_form_of_ownerships_by_invalid_field(client):
    """
    Тест попытки сортировки по несуществующему полю.
    """
    response = client.get(
        "/form-of-ownership", params={"sortBy": "invalid_field", "sortDir": "asc"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Поле не найдено"
