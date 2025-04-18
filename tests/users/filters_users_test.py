def test_filter_users(client, sample_user, another_user):
    response = client.get(
        "/users",
        params={"first_name": [sample_user.first_name, another_user.first_name]},
    )
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

    response = client.get(
        "/users", params={"last_name": [sample_user.last_name, another_user.last_name]}
    )
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

    response = client.get(
        "/users",
        params={"father_name": [sample_user.father_name, another_user.father_name]},
    )
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

    response = client.get(
        "/users", params={"full_name": [sample_user.full_name, another_user.full_name]}
    )
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

    response = client.get(
        "/users", params={"position": [sample_user.position, another_user.position]}
    )
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

    response = client.get(
        "/users", params={"phone": [sample_user.phone, another_user.phone]}
    )
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

    response = client.get(
        "/users", params={"email": [sample_user.email, another_user.email]}
    )
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

    response = client.get(
        "/users", params={"telegram": [sample_user.telegram, another_user.telegram]}
    )
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

    response = client.get(
        "/users", params={"birthday": [sample_user.birthday, another_user.birthday]}
    )
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

    response = client.get(
        "/users", params={"category": [sample_user.category, another_user.category]}
    )
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

    response = client.get(
        "/users",
        params={
            "specialization": [sample_user.specialization, another_user.specialization]
        },
    )
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

    response = client.get(
        "/users", params={"username": [sample_user.username, another_user.username]}
    )
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

    response = client.get(
        "/users", params={"password": [sample_user.password, another_user.password]}
    )
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

    response = client.get(
        "/users", params={"notes": [sample_user.notes, another_user.notes]}
    )
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

    response = client.get(
        "/users", params={"role": [sample_user.role, another_user.role]}
    )
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
            ),
            "category": sample_user.category,
            "specialization": sample_user.specialization,
            "username": sample_user.username,
            "password": None,
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
            "password": None,  # Use the actual password field
            "notes": another_user.notes,
            "role": another_user.role,
            "notification": another_user.notification,
        },
    ]

    response = client.get(
        "/users",
        params={"notification": [sample_user.notification, another_user.notification]},
    )
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
            ),
            "category": sample_user.category,
            "specialization": sample_user.specialization,
            "username": sample_user.username,
            "password": None,
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
            "password": None,  # Use the actual password field
            "notes": another_user.notes,
            "role": another_user.role,
            "notification": another_user.notification,
        },
    ]
