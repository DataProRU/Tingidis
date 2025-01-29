from fastapi import HTTPException, APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from web_app.database import get_db
from sqlalchemy.future import select
from web_app.models.person_contacts import PersonContracts
from web_app.schemas.person_contracts import (
    PersonContractCreate,
    PersonContractResponse,
)
from web_app.middlewares.auth_middleware import token_verification_dependency

router = APIRouter()


# Endpoints
@router.get("/person-contracts", response_model=List[PersonContractResponse])
async def get_person_contracts(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    stmt = select(PersonContracts)
    result = await db.execute(stmt)
    objects = result.scalars().all()
    return objects


@router.get(
    "/person-contracts/{person_contract_id}", response_model=PersonContractResponse
)
async def get_person_contract_by_id(
    person_contract_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(PersonContracts).filter(PersonContracts.id == person_contract_id)
    )
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Контракт не найден")
    return obj


@router.post(
    "/person-contracts",
    response_model=PersonContractResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_person_contract(
    person_contract_data: PersonContractCreate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    obj = PersonContracts(**person_contract_data.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.patch(
    "/person-contracts/{person_contract_id}", response_model=PersonContractResponse
)
async def update_person_contract(
    person_contract_id: int,
    object_data: PersonContractCreate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(PersonContracts).filter(PersonContracts.id == person_contract_id)
    )
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Контракт не найден")

    for key, value in object_data.dict(exclude_unset=True).items():
        setattr(obj, key, value)

    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete(
    "/person-contracts/{person_contract_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_object(
    person_contract_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    # Проверка наличия объекта
    result = await db.execute(
        select(PersonContracts).filter(PersonContracts.id == person_contract_id)
    )
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Контракт не найден")

    # Удаление объекта
    await db.delete(obj)
    await db.commit()
    return {
        "message": "Контракт успешно удален",
        "person_contract_id": person_contract_id,
    }
