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
        "birthday": (
            user.birthday.isoformat() if user.birthday else None
        ),  # Convert date to string
        "category": user.category,
        "specialization": user.specialization,
        "username": user.username,
        "password": None,  # Use the actual password field
        "notes": user.notes,
        "role": user.role,
        "notification": user.notification,
    }

    assert response.json() == expected_response


def test_get_user_by_admin(admin_client, sample_user):
    user = sample_user
    response = admin_client.get(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "father_name": user.father_name,
        "full_name": user.full_name,
        "position": user.position,
        "phone": user.phone,
        "email": user.email,
        "telegram": user.telegram,
        "birthday": (
            user.birthday.isoformat() if user.birthday else None
        ),  # Convert date to string
        "category": user.category,
        "specialization": user.specialization,
        "username": user.username,
        "password": user.password,  # Use the actual password field
        "notes": user.notes,
        "role": user.role,
        "notification": user.notification,
    }


def test_get_all_users_by_admin(admin_client, admin_user, sample_user, another_user):
    response = admin_client.get("/users")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": admin_user.id,
            "first_name": admin_user.first_name,
            "last_name": admin_user.last_name,
            "father_name": admin_user.father_name,
            "full_name": admin_user.full_name,
            "position": admin_user.position,
            "phone": admin_user.phone,
            "email": admin_user.email,
            "telegram": admin_user.telegram,
            "birthday": (
                admin_user.birthday.isoformat() if admin_user.birthday else None
            ),  # Convert date to string
            "category": admin_user.category,
            "specialization": admin_user.specialization,
            "username": admin_user.username,
            "password": admin_user.password,  # Use the actual password field
            "notes": admin_user.notes,
            "role": admin_user.role,
            "notification": admin_user.notification,
        },
        {
            "id": sample_user.id,
            "first_name": sample_user.first_name,
            "last_name": sample_user.last_name,
            "father_name": sample_user.father_name,
            "full_name": sample_user.full_name,
            "position": sample_user.position,
            "phone": sample_user.phone,
            "email": sample_user.email,
            "telegram": sample_user.telegram,
            "birthday": (
                sample_user.birthday.isoformat() if sample_user.birthday else None
            ),  # Convert date to string
            "category": sample_user.category,
            "specialization": sample_user.specialization,
            "username": sample_user.username,
            "password": sample_user.password,  # Use the actual password field
            "notes": sample_user.notes,
            "role": sample_user.role,
            "notification": sample_user.notification,
        },
        {
            "id": another_user.id,
            "first_name": another_user.first_name,
            "last_name": another_user.last_name,
            "father_name": another_user.father_name,
            "full_name": another_user.full_name,
            "position": another_user.position,
            "phone": another_user.phone,
            "email": another_user.email,
            "telegram": another_user.telegram,
            "birthday": (
                another_user.birthday.isoformat() if another_user.birthday else None
            ),  # Convert date to string
            "category": another_user.category,
            "specialization": another_user.specialization,
            "username": another_user.username,
            "password": another_user.password,  # Use the actual password field
            "notes": another_user.notes,
            "role": another_user.role,
            "notification": another_user.notification,
        },
    ]


def test_get_all_users_by_user_role(client, admin_user, sample_user, another_user):
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": sample_user.id,
            "first_name": sample_user.first_name,
            "last_name": sample_user.last_name,
            "father_name": sample_user.father_name,
            "full_name": sample_user.full_name,
            "position": sample_user.position,
            "phone": sample_user.phone,
            "email": sample_user.email,
            "telegram": sample_user.telegram,
            "birthday": (
                sample_user.birthday.isoformat() if sample_user.birthday else None
            ),  # Convert date to string
            "category": sample_user.category,
            "specialization": sample_user.specialization,
            "username": sample_user.username,
            "password": None,  # Use the actual password field
            "notes": sample_user.notes,
            "role": sample_user.role,
            "notification": sample_user.notification,
        },
        {
            "id": admin_user.id,
            "first_name": admin_user.first_name,
            "last_name": admin_user.last_name,
            "father_name": admin_user.father_name,
            "full_name": admin_user.full_name,
            "position": admin_user.position,
            "phone": admin_user.phone,
            "email": admin_user.email,
            "telegram": admin_user.telegram,
            "birthday": (
                admin_user.birthday.isoformat() if admin_user.birthday else None
            ),  # Convert date to string
            "category": admin_user.category,
            "specialization": admin_user.specialization,
            "username": admin_user.username,
            "password": None,  # Use the actual password field
            "notes": admin_user.notes,
            "role": admin_user.role,
            "notification": another_user.notification,
        },
        {
            "id": another_user.id,
            "first_name": another_user.first_name,
            "last_name": another_user.last_name,
            "father_name": another_user.father_name,
            "full_name": another_user.full_name,
            "position": another_user.position,
            "phone": another_user.phone,
            "email": another_user.email,
            "telegram": another_user.telegram,
            "birthday": (
                another_user.birthday.isoformat() if another_user.birthday else None
            ),  # Convert date to string
            "category": another_user.category,
            "specialization": another_user.specialization,
            "username": another_user.username,
            "password": None,  # Use the actual password field
            "notes": another_user.notes,
            "role": another_user.role,
            "notification": another_user.notification,
        },
    ]


def test_unauthenticated_user_cannot_read_user(client, sample_user):
    client.headers = {}
    user = sample_user
    assert sample_user.id == 1
    response = client.get(f"/users/{user.id}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Отсутствует токен"}
