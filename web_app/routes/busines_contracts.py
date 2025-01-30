from fastapi import HTTPException, APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from web_app.database import get_db
from sqlalchemy.future import select
from web_app.models.business_contracts import BusinessContracts
from web_app.schemas.business_contracts import (
    BusinessContractsCreate,
    BusinessContractsResponse,
)
from web_app.middlewares.auth_middleware import token_verification_dependency

router = APIRouter()


# Endpoints
@router.get("/business-contracts", response_model=List[BusinessContractsResponse])
async def get_business_contracts(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    stmt = select(BusinessContracts)
    result = await db.execute(stmt)
    objects = result.scalars().all()
    return objects


@router.get(
    "/business-contracts/{business_contract_id}",
    response_model=BusinessContractsResponse,
)
async def get_business_contract_by_id(
    business_contract_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(BusinessContracts).filter(BusinessContracts.id == business_contract_id)
    )
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Контракт не найден")
    return obj


@router.post(
    "/business-contracts",
    response_model=BusinessContractsResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_object(
    object_data: BusinessContractsCreate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    obj = BusinessContracts(**object_data.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.patch(
    "/business-contracts/{business_contract_id}",
    response_model=BusinessContractsResponse,
)
async def update_business_contract(
    business_contract_id: int,
    object_data: BusinessContractsCreate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(BusinessContracts).filter(BusinessContracts.id == business_contract_id)
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
    "/business-contracts/{business_contract_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_object(
    business_contract_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    # Проверка наличия объекта
    result = await db.execute(
        select(BusinessContracts).filter(BusinessContracts.id == business_contract_id)
    )
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Контракт не найден")

    # Удаление объекта
    await db.delete(obj)
    await db.commit()
    return {
        "message": "Объект успешно удален",
        "business_contract_id": business_contract_id,
    }
