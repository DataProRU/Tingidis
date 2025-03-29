def test_filter_users(client, sample_user, another_user, third_user):
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
        {
            "id": third_user.id,
            "first_name": third_user.first_name,
            "last_name": third_user.last_name,
            "father_name": third_user.father_name,
            "full_name": third_user.full_name,
            "position": third_user.position,
            "phone": third_user.phone,
            "email": third_user.email,
            "telegram": third_user.telegram,
            "birthday": (
                third_user.birthday.isoformat() if third_user.birthday else None
            ),  # Convert date to string
            "category": third_user.category,
            "specialization": third_user.specialization,
            "username": third_user.username,
            "password": None,  # Use the actual password field
            "notes": third_user.notes,
            "role": third_user.role,
            "notification": third_user.notification,
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
        {
            "id": third_user.id,
            "first_name": third_user.first_name,
            "last_name": third_user.last_name,
            "father_name": third_user.father_name,
            "full_name": third_user.full_name,
            "position": third_user.position,
            "phone": third_user.phone,
            "email": third_user.email,
            "telegram": third_user.telegram,
            "birthday": (
                third_user.birthday.isoformat() if third_user.birthday else None
            ),  # Convert date to string
            "category": third_user.category,
            "specialization": third_user.specialization,
            "username": third_user.username,
            "password": None,  # Use the actual password field
            "notes": third_user.notes,
            "role": third_user.role,
            "notification": third_user.notification,
        },
    ]

    response = client.get(
        "/users", params={"position": [sample_user.position, another_user.position]}
    )
    assert response.status_code == 200
    assert response.json() == [
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
        {
            "id": third_user.id,
            "first_name": third_user.first_name,
            "last_name": third_user.last_name,
            "father_name": third_user.father_name,
            "full_name": third_user.full_name,
            "position": third_user.position,
            "phone": third_user.phone,
            "email": third_user.email,
            "telegram": third_user.telegram,
            "birthday": (
                third_user.birthday.isoformat() if third_user.birthday else None
            ),  # Convert date to string
            "category": third_user.category,
            "specialization": third_user.specialization,
            "username": third_user.username,
            "password": None,  # Use the actual password field
            "notes": third_user.notes,
            "role": third_user.role,
            "notification": third_user.notification,
        },
    ]

    response = client.get(
        "/users", params={"phone": [sample_user.phone, another_user.phone]}
    )
    assert response.status_code == 200
    assert response.json() == [
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
        {
            "id": third_user.id,
            "first_name": third_user.first_name,
            "last_name": third_user.last_name,
            "father_name": third_user.father_name,
            "full_name": third_user.full_name,
            "position": third_user.position,
            "phone": third_user.phone,
            "email": third_user.email,
            "telegram": third_user.telegram,
            "birthday": (
                third_user.birthday.isoformat() if third_user.birthday else None
            ),  # Convert date to string
            "category": third_user.category,
            "specialization": third_user.specialization,
            "username": third_user.username,
            "password": None,  # Use the actual password field
            "notes": third_user.notes,
            "role": third_user.role,
            "notification": third_user.notification,
        },
    ]

    response = client.get(
        "/users", params={"email": [sample_user.email, another_user.email]}
    )
    assert response.status_code == 200
    assert response.json() == [
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
        {
            "id": third_user.id,
            "first_name": third_user.first_name,
            "last_name": third_user.last_name,
            "father_name": third_user.father_name,
            "full_name": third_user.full_name,
            "position": third_user.position,
            "phone": third_user.phone,
            "email": third_user.email,
            "telegram": third_user.telegram,
            "birthday": (
                third_user.birthday.isoformat() if third_user.birthday else None
            ),  # Convert date to string
            "category": third_user.category,
            "specialization": third_user.specialization,
            "username": third_user.username,
            "password": None,  # Use the actual password field
            "notes": third_user.notes,
            "role": third_user.role,
            "notification": third_user.notification,
        },
    ]

    response = client.get(
        "/users", params={"telegram": [sample_user.telegram, another_user.telegram]}
    )
    assert response.status_code == 200
    assert response.json() == [
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
        {
            "id": third_user.id,
            "first_name": third_user.first_name,
            "last_name": third_user.last_name,
            "father_name": third_user.father_name,
            "full_name": third_user.full_name,
            "position": third_user.position,
            "phone": third_user.phone,
            "email": third_user.email,
            "telegram": third_user.telegram,
            "birthday": (
                third_user.birthday.isoformat() if third_user.birthday else None
            ),  # Convert date to string
            "category": third_user.category,
            "specialization": third_user.specialization,
            "username": third_user.username,
            "password": None,  # Use the actual password field
            "notes": third_user.notes,
            "role": third_user.role,
            "notification": third_user.notification,
        },
    ]

    response = client.get(
        "/users", params={"birthday": [another_user.birthday, third_user.birthday]}
    )
    assert response.status_code == 200
    assert response.json() == [
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
        {
            "id": third_user.id,
            "first_name": third_user.first_name,
            "last_name": third_user.last_name,
            "father_name": third_user.father_name,
            "full_name": third_user.full_name,
            "position": third_user.position,
            "phone": third_user.phone,
            "email": third_user.email,
            "telegram": third_user.telegram,
            "birthday": (
                third_user.birthday.isoformat() if third_user.birthday else None
            ),  # Convert date to string
            "category": third_user.category,
            "specialization": third_user.specialization,
            "username": third_user.username,
            "password": None,  # Use the actual password field
            "notes": third_user.notes,
            "role": third_user.role,
            "notification": third_user.notification,
        },
    ]

    response = client.get(
        "/users", params={"category": [another_user.category, third_user.category]}
    )
    assert response.status_code == 200
    assert response.json() == [
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
        {
            "id": third_user.id,
            "first_name": third_user.first_name,
            "last_name": third_user.last_name,
            "father_name": third_user.father_name,
            "full_name": third_user.full_name,
            "position": third_user.position,
            "phone": third_user.phone,
            "email": third_user.email,
            "telegram": third_user.telegram,
            "birthday": (
                third_user.birthday.isoformat() if third_user.birthday else None
            ),  # Convert date to string
            "category": third_user.category,
            "specialization": third_user.specialization,
            "username": third_user.username,
            "password": None,  # Use the actual password field
            "notes": third_user.notes,
            "role": third_user.role,
            "notification": third_user.notification,
        },
    ]

    response = client.get(
        "/users",
        params={
            "specialization": [another_user.specialization, third_user.specialization]
        },
    )
    assert response.status_code == 200
    assert response.json() == [
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
        {
            "id": third_user.id,
            "first_name": third_user.first_name,
            "last_name": third_user.last_name,
            "father_name": third_user.father_name,
            "full_name": third_user.full_name,
            "position": third_user.position,
            "phone": third_user.phone,
            "email": third_user.email,
            "telegram": third_user.telegram,
            "birthday": (
                third_user.birthday.isoformat() if third_user.birthday else None
            ),  # Convert date to string
            "category": third_user.category,
            "specialization": third_user.specialization,
            "username": third_user.username,
            "password": None,  # Use the actual password field
            "notes": third_user.notes,
            "role": third_user.role,
            "notification": third_user.notification,
        },
    ]

    response = client.get(
        "/users", params={"username": [another_user.username, third_user.username]}
    )
    assert response.status_code == 200
    assert response.json() == [
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
        {
            "id": third_user.id,
            "first_name": third_user.first_name,
            "last_name": third_user.last_name,
            "father_name": third_user.father_name,
            "full_name": third_user.full_name,
            "position": third_user.position,
            "phone": third_user.phone,
            "email": third_user.email,
            "telegram": third_user.telegram,
            "birthday": (
                third_user.birthday.isoformat() if third_user.birthday else None
            ),  # Convert date to string
            "category": third_user.category,
            "specialization": third_user.specialization,
            "username": third_user.username,
            "password": None,  # Use the actual password field
            "notes": third_user.notes,
            "role": third_user.role,
            "notification": third_user.notification,
        },
    ]

    response = client.get(
        "/users", params={"password": [another_user.password, third_user.password]}
    )
    assert response.status_code == 200
    assert response.json() == [
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
        {
            "id": third_user.id,
            "first_name": third_user.first_name,
            "last_name": third_user.last_name,
            "father_name": third_user.father_name,
            "full_name": third_user.full_name,
            "position": third_user.position,
            "phone": third_user.phone,
            "email": third_user.email,
            "telegram": third_user.telegram,
            "birthday": (
                third_user.birthday.isoformat() if third_user.birthday else None
            ),  # Convert date to string
            "category": third_user.category,
            "specialization": third_user.specialization,
            "username": third_user.username,
            "password": None,  # Use the actual password field
            "notes": third_user.notes,
            "role": third_user.role,
            "notification": third_user.notification,
        },
    ]

    response = client.get(
        "/users", params={"notes": [another_user.notes, third_user.notes]}
    )
    assert response.status_code == 200
    assert response.json() == [
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
        {
            "id": third_user.id,
            "first_name": third_user.first_name,
            "last_name": third_user.last_name,
            "father_name": third_user.father_name,
            "full_name": third_user.full_name,
            "position": third_user.position,
            "phone": third_user.phone,
            "email": third_user.email,
            "telegram": third_user.telegram,
            "birthday": (
                third_user.birthday.isoformat() if third_user.birthday else None
            ),  # Convert date to string
            "category": third_user.category,
            "specialization": third_user.specialization,
            "username": third_user.username,
            "password": None,  # Use the actual password field
            "notes": third_user.notes,
            "role": third_user.role,
            "notification": third_user.notification,
        },
    ]

    response = client.get(
        "/users", params={"role": [another_user.role, third_user.role]}
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
        {
            "id": third_user.id,
            "first_name": third_user.first_name,
            "last_name": third_user.last_name,
            "father_name": third_user.father_name,
            "full_name": third_user.full_name,
            "position": third_user.position,
            "phone": third_user.phone,
            "email": third_user.email,
            "telegram": third_user.telegram,
            "birthday": (
                third_user.birthday.isoformat() if third_user.birthday else None
            ),  # Convert date to string
            "category": third_user.category,
            "specialization": third_user.specialization,
            "username": third_user.username,
            "password": None,  # Use the actual password field
            "notes": third_user.notes,
            "role": third_user.role,
            "notification": third_user.notification,
        },
    ]

    response = client.get(
        "/users",
        params={"notification": [another_user.notification, third_user.notification]},
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
        {
            "id": third_user.id,
            "first_name": third_user.first_name,
            "last_name": third_user.last_name,
            "father_name": third_user.father_name,
            "full_name": third_user.full_name,
            "position": third_user.position,
            "phone": third_user.phone,
            "email": third_user.email,
            "telegram": third_user.telegram,
            "birthday": (
                third_user.birthday.isoformat() if third_user.birthday else None
            ),  # Convert date to string
            "category": third_user.category,
            "specialization": third_user.specialization,
            "username": third_user.username,
            "password": None,  # Use the actual password field
            "notes": third_user.notes,
            "role": third_user.role,
            "notification": third_user.notification,
        },
    ]
