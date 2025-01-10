from datetime import date

import pytest

from web_app.database import WebUser

@pytest.fixture
async def sample_user(db):
    # Create a new user by directly passing data to the model
    new_user = WebUser(
        username="user",
        last_name="Ivan",
        first_name="Ivanov",
        full_name="Ivan Ivanovich",
        middle_name="Ivanovich",
        position="Engineer",
        phone="+7 (911) 481 00 52",
        email="ivanov@mail.com",
        telegram="@ivan",
        birthdate=date(2024, 1, 1),
        category="test user",
        specialization="Engineering",
        notes="test user",
        login="user",
        password="123456789",  # Don't forget to hash the password
        role="user",
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
