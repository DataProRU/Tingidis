def test_update_user(client, sample_user):
    user = sample_user
    payload = {
        "first_name": "Alex_new",
        "last_name": "Alexeev_new",
        "father_name": "Ivanovich_new",
        "full_name": "Alex Ivanovich_new",
        "position": "Worker_new",
        "phone": "+3 (911) 181 00 00",
        "email": "alex@mail.com_new",
        "telegram": "@alex_new",
        "birthday": "2001-02-01",
        "category": "test user new",
        "specialization": "Working_new",
        "username": "user_alex_new",
        "password": "123456789qqFF_999",
        "notes": "another test user_new",
        "role": "admin"
    }
    response = client.patch(f"/users/{user.id}", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["first_name"] == "Alex_new"
    assert result["last_name"] == "Alexeev_new"
    assert result["father_name"] == "Ivanovich_new"
    assert result["position"] == "Worker_new"
    assert result["phone"] == "+3 (911) 181 00 00"
    assert result["email"] == "alex@mail.com_new"
    assert result["telegram"] == "@alex_new"
    assert result["birthday"] == "2001-02-01"
    assert result["category"] == "test user new"
    assert result["specialization"] == "Working_new"
    assert result["username"] == "user_alex_new"
    assert result["password"] == "123456789qqFF_999"
    assert result["notes"] == "another test user_new"
    assert result["role"] == "admin"


def test_unauthenticated_user_cannot_update_user(client, sample_user):
    user = sample_user
    client.headers = {}
    payload = {
        "first_name": "Alex_new",
        "last_name": "Alexeev_new",
        "father_name": "Ivanovich_new",
        "full_name": "Alex Ivanovich_new",
        "position": "Worker_new",
        "phone": "+3 (911) 181 00 00",
        "email": "alex@mail.com_new",
        "telegram": "@alex_new",
        "birthday": "2001-02-01",
        "category": "test user new",
        "specialization": "Working_new",
        "username": "user_alex_new",
        "password": "123456789qqFF_999",
        "notes": "another test user_new",
        "role": "admin"
    }
    response = client.patch(f"/users/{user.id}", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
