'''def test_get_empty_user(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == []'''

def test_unauthenticated_user_cannot_read_users(client):
    client.headers = {}
    response = client.get("/users/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}

def test_get_user(client, another_user):
    user = another_user
    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200

    expected_response = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "father_name": user.father_name,
        "full_name": user.full_name,
        "position": user.position,
        "phone": user.phone,
        "email": user.email,
        "telegram": user.telegram,
        "birthday": user.birthday.isoformat() if user.birthday else None,  # Convert date to string
        "category": user.category,
        "specialization": user.specialization,
        "username": user.username,
        "password": user.password,  # Use the actual password field
        "notes": user.notes,
        "role": user.role
    }

    assert response.json() == expected_response

def test_get_user(client, sample_user):
    user = sample_user
    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json() == {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "father_name": user.father_name,
        "full_name": user.full_name,
        "position": user.position,
        "phone": user.phone,
        "email": user.email,
        "telegram": user.telegram,
        "birthday": user.birthday.isoformat() if user.birthday else None,  # Convert date to string
        "category": user.category,
        "specialization": user.specialization,
        "username": user.username,
        "password": user.password,  # Use the actual password field
        "notes": user.notes,
        "role": user.role
    }

def test_unauthenticated_user_cannot_read_user(client, sample_user):
    client.headers = {}
    user = sample_user
    response = client.get(f"/users/{user.id}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
