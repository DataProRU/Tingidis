from fastapi import HTTPException, APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from web_app.database import get_db
from sqlalchemy.future import select
from web_app.models import Agreements
from web_app.schemas.agreements import (
    AgreementsResponse,
    AgreementsCreate,
)
from web_app.middlewares.auth_middleware import token_verification_dependency
from .utils import log_action

router = APIRouter()


@router.get("/agreements", response_model=List[AgreementsResponse])
async def get_agreements(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    stmt = select(Agreements)
    result = await db.execute(stmt)
    agreements = result.scalars().all()
    return agreements


@router.get("/agreements/{agreements_id}", response_model=AgreementsResponse)
async def get_agreements_by_id(
    agreements_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(select(Agreements).filter(Agreements.id == agreements_id))
    agreement = result.scalar_one_or_none()
    if not agreement:
        raise HTTPException(status_code=404, detail="Соглашение не найдено")
    return agreement


@router.post(
    "/agreements",
    response_model=AgreementsResponse,
    status_code=status.HTTP_201_CREATED,
)
@log_action("Создание соглашения")
async def create_agreement(
    agreement_data: AgreementsCreate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    agreement = Agreements(**agreement_data.dict())
    db.add(agreement)
    await db.commit()
    await db.refresh(agreement)
    return agreement


@router.patch("/agreements/{agreement_id}", response_model=AgreementsResponse)
@log_action("Обновление соглашения")
async def update_agreement(
    agreement_id: int,
    agreement_data: AgreementsCreate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(select(Agreements).filter(Agreements.id == agreement_id))
    agreement = result.scalar_one_or_none()
    if not agreement:
        raise HTTPException(status_code=404, detail="Соглашение не найдено")

    for key, value in agreement_data.dict(exclude_unset=True).items():
        setattr(agreement, key, value)

    await db.commit()
    await db.refresh(agreement)
    return agreement


@router.delete("/agreements/{agreement_id}", status_code=status.HTTP_204_NO_CONTENT)
@log_action("Удаление соглашения")
async def delete_agreement(
    agreement_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    # Проверка наличия объекта
    result = await db.execute(select(Agreements).filter(Agreements.id == agreement_id))
    agreement = result.scalar_one_or_none()
    if not agreement:
        raise HTTPException(status_code=404, detail="Соглашение не найдено")

    # Удаление объекта
    await db.delete(agreement)
    await db.commit()
    return {"message": "Соглашение успешно удалено", "agreement_id": agreement_id}
