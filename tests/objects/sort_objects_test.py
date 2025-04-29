import pytest


@pytest.mark.asyncio
async def test_sort_objects_by_code_asc(
    client, sample_object, another_object, third_object
):
    """
    Тест сортировки клиентов по (code) в порядке возрастания.
    """
    response = client.get("/objects", params={"sortBy": "code", "sortDir": "asc"})
    assert response.status_code == 200

    customers = response.json()
    assert customers[0]["code"] == "123456"
    assert customers[1]["code"] == "123457"
    assert customers[2]["code"] == "345678"


@pytest.mark.asyncio
async def test_sort_objects_by_code_desc(
    client, sample_object, another_object, third_object
):
    """
    Тест сортировки клиентов по (code) в порядке убыванию.
    """
    response = client.get("/objects", params={"sortBy": "code", "sortDir": "desc"})
    assert response.status_code == 200

    customers = response.json()
    assert customers[0]["code"] == "345678"
    assert customers[1]["code"] == "123457"
    assert customers[2]["code"] == "123456"


@pytest.mark.asyncio
async def test_sort_objects_by_name_asc(
    client, sample_object, another_object, third_object
):
    """
    Тест сортировки клиентов по (name) в порядке возрастания.
    """
    response = client.get("/objects", params={"sortBy": "name", "sortDir": "asc"})
    assert response.status_code == 200

    customers = response.json()
    assert customers[0]["name"] == "test name"
    assert customers[1]["name"] == "test name 2"
    assert customers[2]["name"] == "third object"


@pytest.mark.asyncio
async def test_sort_objects_by_name_desc(
    client, sample_object, another_object, third_object
):
    """
    Тест сортировки клиентов по (name) в порядке убыванию.
    """
    response = client.get("/objects", params={"sortBy": "name", "sortDir": "desc"})
    assert response.status_code == 200

    customers = response.json()
    assert customers[0]["name"] == "third object"
    assert customers[1]["name"] == "test name 2"
    assert customers[2]["name"] == "test name"


@pytest.mark.asyncio
async def test_sort_objects_by_comment_asc(
    client, sample_object, another_object, third_object
):
    """
    Тест сортировки клиентов по (comment) в порядке возрастания.
    """
    response = client.get("/objects", params={"sortBy": "comment", "sortDir": "asc"})
    assert response.status_code == 200

    customers = response.json()
    assert customers[0]["comment"] == "OBJ 1 notes"
    assert customers[1]["comment"] == "test comment 2"
    assert customers[2]["comment"] == "third object comment"


@pytest.mark.asyncio
async def test_sort_objects_by_comment_desc(
    client, sample_object, another_object, third_object
):
    """
    Тест сортировки клиентов по (comment) в порядке убыванию.
    """
    response = client.get("/objects", params={"sortBy": "comment", "sortDir": "desc"})
    assert response.status_code == 200

    customers = response.json()
    assert customers[0]["comment"] == "third object comment"
    assert customers[1]["comment"] == "test comment 2"
    assert customers[2]["comment"] ==  "OBJ 1 notes"
