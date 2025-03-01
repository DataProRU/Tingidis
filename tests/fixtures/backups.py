from datetime import date

import pytest

from web_app.models import Backups


@pytest.fixture
async def sample_backup(async_session_test):
    async with async_session_test() as db:
        backup = Backups(
            email="test@test.com",
            frequency=2,
            send_date=date(2024, 1, 1),
        )
        db.add(backup)
        await db.commit()
        await db.refresh(backup)
        return backup


@pytest.fixture
async def another_backup(async_session_test):
    async with async_session_test() as db:
        backup = Backups(
            email="test2@test.com",
            frequency=3,
            send_date=date(2024, 1, 2),
        )
        db.add(backup)
        await db.commit()
        await db.refresh(backup)
        return backup
