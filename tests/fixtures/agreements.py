from datetime import date
import pytest

from web_app.models.agreements import Agreements


@pytest.fixture
async def create_agreement(async_session_test):
    """
    Универсальная фикстура для создания соглашений с заданными параметрами.
    """

    async def _create_agreement(
        name: str,
        number: str,
        price: int,
        deadline: date,
        notes: str = None,
        contract_id: int = None,
    ):
        async with async_session_test() as db:
            agreement = Agreements(
                name=name,
                number=number,
                price=price,
                deadline=deadline,
                notes=notes,
                contract=contract_id,
            )
            db.add(agreement)
            await db.commit()
            await db.refresh(agreement)
            return agreement

    return _create_agreement


@pytest.fixture
async def sample_agreement(create_agreement, another_contract):
    """
    Фикстура для создания тестового соглашения.
    """
    return await create_agreement(
        name="test_agreement",
        number="1234567890",
        price=1000,
        deadline=date(2024, 1, 1),
        notes=None,
        contract_id=another_contract.id,
    )


@pytest.fixture
async def another_agreement(create_agreement, sample_contract):
    """
    Фикстура для создания другого тестового соглашения.
    """
    return await create_agreement(
        name="new_test_agreement",
        number="987654321",
        price=1500,
        deadline=date(2024, 2, 2),
        notes="new_test notes",
        contract_id=sample_contract.id,
    )


@pytest.fixture
async def third_agreement(create_agreement, fourth_contract):
    """
    Фикстура для создания третьего тестового соглашения.
    """
    return await create_agreement(
        name="third_agreement",
        number="11111",
        price=2000,
        deadline=date(2025, 3, 3),
        notes="third notes",
        contract_id=fourth_contract.id,
    )


@pytest.fixture
async def fourth_agreement(create_agreement, third_contract):
    """
    Фикстура для создания четвертого тестового соглашения.
    """
    return await create_agreement(
        name="fourth_agreement",
        number="22222",
        price=5000,
        deadline=date(2026, 4, 4),
        notes="fourth notes",
        contract_id=third_contract.id,
    )
