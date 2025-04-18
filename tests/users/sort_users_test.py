import pytest
from datetime import date


@pytest.mark.asyncio
async def test_sort_users_by_username_asc(client, sample_user, another_user):
    """
    Тест сортировки пользователей по имени пользователя (username) в порядке возрастания.
    """
    response = client.get("/users", params={"sortBy": "username", "sortDir": "asc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["username"] == sample_user.username  # "user"
    assert users[1]["username"] == another_user.username  # "user_alex"


@pytest.mark.asyncio
async def test_sort_users_by_username_desc(client, sample_user, another_user):
    """
    Тест сортировки пользователей по имени пользователя (username) в порядке убывания.
    """
    response = client.get("/users", params={"sortBy": "username", "sortDir": "desc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["username"] == another_user.username  # "user_alex"
    assert users[1]["username"] == sample_user.username  # "user"


@pytest.mark.asyncio
async def test_sort_users_by_full_name_asc(client, another_user, sample_user):
    """
    Тест сортировки пользователей по полному имени (full_name) в порядке возрастания.
    """
    response = client.get("/users", params={"sortBy": "full_name", "sortDir": "asc"})
    assert response.status_code == 200

    users = response.json()
    assert users[0]["full_name"] == another_user.full_name  # "Alex Ivanovich"
    assert users[1]["full_name"] == sample_user.full_name  # "Maria Petrovna Sidorova"


@pytest.mark.asyncio
async def test_sort_users_by_birthday_asc(
    client, another_user, third_user, sample_user, fourth_user
):
    """
    Тест сортировки пользователей по дате рождения (birthday) в порядке возрастания.
    """
    response = client.get("/users", params={"sortBy": "birthday", "sortDir": "asc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 3
    assert users[0]["birthday"] == sample_user.birthday.isoformat()  # "1981-12-30"
    assert users[1]["birthday"] == fourth_user.birthday.isoformat()  # "1985-11-30"
    assert users[2]["birthday"] == third_user.birthday.isoformat()  # "1995-05-15"


@pytest.mark.asyncio
async def test_sort_users_by_role_asc(client, sample_user, admin_user):
    """
    Тест сортировки пользователей по роли (role) в порядке возрастания.
    """
    response = client.get("/users", params={"sortBy": "role", "sortDir": "asc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["role"] == admin_user.role  # "admin"
    assert users[1]["role"] == sample_user.role  # "user"


@pytest.mark.asyncio
async def test_sort_users_by_invalid_field(client):
    """
    Тест попытки сортировки по несуществующему полю.
    """
    response = client.get(
        "/users", params={"sortBy": "invalid_field", "sortDir": "asc"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Поле не найдено"
