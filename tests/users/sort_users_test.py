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
    assert users[0]["username"] == "user 1"
    assert users[1]["username"] == "user_alex"


@pytest.mark.asyncio
async def test_sort_users_by_username_desc(client, sample_user, another_user):
    """
    Тест сортировки пользователей по имени пользователя (username) в порядке убывания.
    """
    response = client.get("/users", params={"sortBy": "username", "sortDir": "desc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["username"] == "user_alex"
    assert users[1]["username"] == "user 1"


@pytest.mark.asyncio
async def test_sort_users_by_full_name_asc(client, sample_user, another_user):
    """
    Тест сортировки пользователей по полному имени (full_name) в порядке возрастания.
    """
    response = client.get("/users", params={"sortBy": "full_name", "sortDir": "asc"})
    assert response.status_code == 200

    users = response.json()
    assert users[0]["full_name"] == "Alex Ivanovich"
    assert users[1]["full_name"] == "Ivan Ivanovich"


@pytest.mark.asyncio
async def test_sort_users_by_full_name_desc(client, sample_user, another_user):
    """
    Тест сортировки пользователей по полному имени (full_name) в порядке возрастания.
    """
    response = client.get("/users", params={"sortBy": "full_name", "sortDir": "desc"})
    assert response.status_code == 200

    users = response.json()
    assert users[0]["full_name"] == "Ivan Ivanovich"
    assert users[1]["full_name"] == "Alex Ivanovich"


@pytest.mark.asyncio
async def test_sort_users_by_birthday_asc(
    client, third_user, sample_user, another_user
):
    """
    Тест сортировки пользователей по дате рождения (birthday) в порядке возрастания.
    """
    response = client.get("/users", params={"sortBy": "birthday", "sortDir": "asc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 3
    assert users[0]["birthday"] == date(1981, 12, 30).isoformat()
    assert users[1]["birthday"] == date(1995, 5, 15).isoformat()
    assert users[2]["birthday"] == date(2001, 2, 2).isoformat()


@pytest.mark.asyncio
async def test_sort_users_by_birthday_desc(
    client, another_user, third_user, sample_user
):
    """
    Тест сортировки пользователей по дате рождения (birthday) в порядке возрастания.
    """
    response = client.get("/users", params={"sortBy": "birthday", "sortDir": "desc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 3
    assert users[0]["birthday"] == date(2001, 2, 2).isoformat()
    assert users[1]["birthday"] ==date(1995, 5, 15).isoformat()
    assert users[2]["birthday"] == date(1981, 12, 30).isoformat()


@pytest.mark.asyncio
async def test_sort_users_by_role_asc(client, sample_user, admin_user):
    """
    Тест сортировки пользователей по роли (role) в порядке возрастания.
    """
    response = client.get("/users", params={"sortBy": "role", "sortDir": "asc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["role"] == "admin"
    assert users[1]["role"] == "user"


@pytest.mark.asyncio
async def test_sort_users_by_role_desc(client, sample_user, admin_user):
    """
    Тест сортировки пользователей по роли (role) в порядке возрастания.
    """
    response = client.get("/users", params={"sortBy": "role", "sortDir": "desc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["role"] == "user"
    assert users[1]["role"] == "admin"


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


@pytest.mark.asyncio
async def test_sort_users_by_first_name_asc(client, sample_user, another_user):
    """
    Тест сортировки пользователей по имени (first_name) в порядке возрастания.
    """
    response = client.get("/users", params={"sortBy": "first_name", "sortDir": "asc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["first_name"] == "Alex"
    assert users[1]["first_name"] == "Ivan"


@pytest.mark.asyncio
async def test_sort_users_by_first_name_desc(client, sample_user, another_user):
    """
    Тест сортировки пользователей по имени (first_name) в порядке убывания.
    """
    response = client.get("/users", params={"sortBy": "first_name", "sortDir": "desc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["first_name"] == "Ivan"
    assert users[1]["first_name"] == "Alex"


@pytest.mark.asyncio
async def test_sort_users_by_last_name_asc(client, sample_user, another_user):
    """
    Тест сортировки пользователей по фамилии (last_name) в порядке возрастания.
    """
    response = client.get("/users", params={"sortBy": "last_name", "sortDir": "asc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["last_name"] == "Alexeev"
    assert users[1]["last_name"] == "Ivanov"


@pytest.mark.asyncio
async def test_sort_users_by_last_name_desc(client, sample_user, another_user):
    """
    Тест сортировки пользователей по фамилии (last_name) в порядке убывания.
    """
    response = client.get("/users", params={"sortBy": "last_name", "sortDir": "desc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["last_name"] == "Ivanov"
    assert users[1]["last_name"] == "Alexeev"


@pytest.mark.asyncio
async def test_sort_users_by_father_name_asc(client, sample_user, another_user):
    """
    Тест сортировки пользователей по отчеству (father_name) в порядке возрастания.
    """
    response = client.get("/users", params={"sortBy": "father_name", "sortDir": "asc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["father_name"] == "Alekseevich"
    assert users[1]["father_name"] == "Ivanovich"


@pytest.mark.asyncio
async def test_sort_users_by_father_name_desc(client, sample_user, another_user):
    """
    Тест сортировки пользователей по отчеству (father_name) в порядке убывания.
    """
    response = client.get("/users", params={"sortBy": "father_name", "sortDir": "desc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["father_name"] == "Ivanovich"
    assert users[1]["father_name"] == "Alekseevich"


@pytest.mark.asyncio
async def test_sort_users_by_position_asc(client, sample_user, another_user):
    """
    Тест сортировки пользователей по должности (position) в порядке возрастания.
    """
    response = client.get("/users", params={"sortBy": "position", "sortDir": "asc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["position"] == "painter"
    assert users[1]["position"] == "Worker"


@pytest.mark.asyncio
async def test_sort_users_by_position_desc(client, sample_user, another_user):
    """
    Тест сортировки пользователей по должности (position) в порядке убывания.
    """
    response = client.get("/users", params={"sortBy": "position", "sortDir": "desc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["position"] == "Worker"
    assert users[1]["position"] == "painter"


@pytest.mark.asyncio
async def test_sort_users_by_phone_asc(client, sample_user, another_user):
    """
    Тест сортировки пользователей по телефону (phone) в порядке возрастания.
    """
    response = client.get("/users", params={"sortBy": "phone", "sortDir": "asc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["phone"] == "+3 (911) 181 00 32"
    assert users[1]["phone"] == "+7(911) 337 65 43"


@pytest.mark.asyncio
async def test_sort_users_by_phone_desc(client, sample_user, another_user):
    """
    Тест сортировки пользователей по телефону (phone) в порядке убывания.
    """
    response = client.get("/users", params={"sortBy": "phone", "sortDir": "desc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["phone"] == "+7(911) 337 65 43"
    assert users[1]["phone"] == "+3 (911) 181 00 32"


@pytest.mark.asyncio
async def test_sort_users_by_email_asc(client, sample_user, another_user):
    """
    Тест сортировки пользователей по email в порядке возрастания.
    """
    response = client.get("/users", params={"sortBy": "email", "sortDir": "asc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["email"] == "alex@mail.com"
    assert users[1]["email"] == "ivan@example.com"


@pytest.mark.asyncio
async def test_sort_users_by_email_desc(client, sample_user, another_user):
    """
    Тест сортировки пользователей по email в порядке убывания.
    """
    response = client.get("/users", params={"sortBy": "email", "sortDir": "desc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["email"] == "ivan@example.com"
    assert users[1]["email"] == "alex@mail.com"


@pytest.mark.asyncio
async def test_sort_users_by_telegram_asc(client, sample_user, another_user):
    """
    Тест сортировки пользователей по telegram в порядке возрастания.
    """
    response = client.get("/users", params={"sortBy": "telegram", "sortDir": "asc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["telegram"] == "@alex"
    assert users[1]["telegram"] == "@ivan_paint"


@pytest.mark.asyncio
async def test_sort_users_by_telegram_desc(client, sample_user, another_user):
    """
    Тест сортировки пользователей по telegram в порядке убывания.
    """
    response = client.get("/users", params={"sortBy": "telegram", "sortDir": "desc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["telegram"] == "@ivan_paint"
    assert users[1]["telegram"] == "@alex"


@pytest.mark.asyncio
async def test_sort_users_by_category_asc(client, sample_user, another_user):
    """
    Тест сортировки пользователей по категории (category) в порядке возрастания.
    """
    response = client.get("/users", params={"sortBy": "category", "sortDir": "asc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["category"] == "paint"
    assert users[1]["category"] == "test user"


@pytest.mark.asyncio
async def test_sort_users_by_category_desc(client, sample_user, another_user):
    """
    Тест сортировки пользователей по категории (category) в порядке убывания.
    """
    response = client.get("/users", params={"sortBy": "category", "sortDir": "desc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["category"] == "test user"
    assert users[1]["category"] == "paint"


@pytest.mark.asyncio
async def test_sort_users_by_specialization_asc(client, sample_user, another_user):
    """
    Тест сортировки пользователей по специализации (specialization) в порядке возрастания.
    """
    response = client.get("/users", params={"sortBy": "specialization", "sortDir": "asc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["specialization"] == "Painter house"
    assert users[1]["specialization"] == "Working"


@pytest.mark.asyncio
async def test_sort_users_by_specialization_desc(client, sample_user, another_user):
    """
    Тест сортировки пользователей по специализации (specialization) в порядке убывания.
    """
    response = client.get("/users", params={"sortBy": "specialization", "sortDir": "desc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["specialization"] == "Working"
    assert users[1]["specialization"] == "Painter house"


@pytest.mark.asyncio
async def test_sort_users_by_notification_asc(client, sample_user, admin_user):
    """
    Тест сортировки пользователей по уведомлениям (notification) в порядке возрастания.
    """
    response = client.get("/users", params={"sortBy": "notification", "sortDir": "asc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["notification"] is False
    assert users[1]["notification"] is True


@pytest.mark.asyncio
async def test_sort_users_by_notification_desc(client, sample_user, admin_user):
    """
    Тест сортировки пользователей по уведомлениям (notification) в порядке убывания.
    """
    response = client.get("/users", params={"sortBy": "notification", "sortDir": "desc"})
    assert response.status_code == 200

    users = response.json()
    assert len(users) >= 2
    assert users[0]["notification"] is True
    assert users[1]["notification"] is False
