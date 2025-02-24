from fastapi import HTTPException, APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from web_app.database import get_db
from sqlalchemy.future import select
from web_app.models import Agreements, Contracts
from web_app.schemas.agreements import (
    AgreementsResponse,
    AgreementsCreate,
    AgreementsGetResponse,
)
from web_app.middlewares.auth_middleware import token_verification_dependency
from web_app.utils.logs import log_action

router = APIRouter()


@router.get("/agreements", response_model=List[AgreementsGetResponse])
async def get_agreements(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    stmt = select(Agreements).options(selectinload(Agreements.contract_info))
    result = await db.execute(stmt)
    agreements = result.scalars().all()
    response = []
    for agreement in agreements:
        response.append(
            {
                "id": agreement.id,
                "name": agreement.name,
                "number": agreement.number,
                "price": agreement.price,
                "deadline": agreement.deadline,
                "notes": agreement.notes,
                "contract": {
                    "id": agreement.contract_info.id,
                    "code": agreement.contract_info.code,
                    "name": agreement.contract_info.name,
                    "customer": agreement.contract_info.customer,
                    "executor": agreement.contract_info.executor,
                    "number": agreement.contract_info.number,
                    "sign_date": agreement.contract_info.sign_date,
                    "price": agreement.contract_info.price,
                    "theme": agreement.contract_info.theme,
                    "evolution": agreement.contract_info.evolution,
                },
            }
        )

    return response


@router.get("/agreements/{agreements_id}", response_model=AgreementsGetResponse)
async def get_agreements_by_id(
    agreements_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(Agreements)
        .options(selectinload(Agreements.contract_info))
        .filter(Agreements.id == agreements_id)
    )
    agreement = result.scalar_one_or_none()
    if not agreement:
        raise HTTPException(status_code=404, detail="Соглашение не найдено")

    return {
        "id": agreement.id,
        "name": agreement.name,
        "number": agreement.number,
        "price": agreement.price,
        "deadline": agreement.deadline,
        "notes": agreement.notes,
        "contract": {
            "id": agreement.contract_info.id,
            "code": agreement.contract_info.code,
            "name": agreement.contract_info.name,
            "customer": agreement.contract_info.customer,
            "executor": agreement.contract_info.executor,
            "number": agreement.contract_info.number,
            "sign_date": agreement.contract_info.sign_date,
            "price": agreement.contract_info.price,
            "theme": agreement.contract_info.theme,
            "evolution": agreement.contract_info.evolution,
        },
    }


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


@router.patch("/agreements/{agreement_id}", response_model=AgreementsGetResponse)
@log_action("Обновление соглашения")
async def update_agreement(
    agreement_id: int,
    agreement_data: AgreementsResponse,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(Agreements)
        .options(selectinload(Agreements.contract_info))
        .filter(Agreements.id == agreement_id)
    )
    agreement = result.scalar_one_or_none()
    if not agreement:
        raise HTTPException(status_code=404, detail="Соглашение не найдено")

    for key, value in agreement_data.dict(exclude_unset=True).items():
        setattr(agreement, key, value)

    await db.commit()
    await db.refresh(agreement)
    return {
        "id": agreement.id,
        "name": agreement.name,
        "number": agreement.number,
        "price": agreement.price,
        "deadline": agreement.deadline,
        "notes": agreement.notes,
        "contract": {
            "id": agreement.contract_info.id,
            "code": agreement.contract_info.code,
            "name": agreement.contract_info.name,
            "customer": agreement.contract_info.customer,
            "executor": agreement.contract_info.executor,
            "number": agreement.contract_info.number,
            "sign_date": agreement.contract_info.sign_date,
            "price": agreement.contract_info.price,
            "theme": agreement.contract_info.theme,
            "evolution": agreement.contract_info.evolution,
        },
    }


@router.delete("/agreements/{object_id}", status_code=status.HTTP_204_NO_CONTENT)
@log_action("Удаление соглашения")
async def delete_agreement(
    object_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    # Проверка наличия объекта
    result = await db.execute(select(Agreements).filter(Agreements.id == object_id))
    agreement = result.scalar_one_or_none()
    if not agreement:
        raise HTTPException(status_code=404, detail="Соглашение не найдено")

    # Удаление объекта
    await db.delete(agreement)
    await db.commit()
    return {"message": "Соглашение успешно удалено", "agreement_id": object_id}
