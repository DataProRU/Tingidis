from datetime import date

import pytest

from web_app.schemas.agreements import AgreementsModel


@pytest.fixture
async def sample_agreement(async_session_test, another_contract):
    async with async_session_test() as db:
        agreement = AgreementsModel(
            name="test_agreement",
            number="1234567890",
            deadline=date(2024, 1, 1),
            notes="test notes",
            contract=another_contract.id,
        )
        db.add(agreement)
        await db.commit()
        await db.refresh(agreement)
        return agreement


@pytest.fixture
async def another_agreement(async_session_test, sample_contract):
    async with async_session_test() as db:
        agreement = AgreementsModel(
            name="new_test_agreement",
            number="987654321",
            deadline=date(2024, 2, 2),
            notes="new_test notes",
            contract=sample_contract.id,
        )
        db.add(agreement)
        await db.commit()
        await db.refresh(agreement)
        return agreement
