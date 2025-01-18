from fastapi import FastAPI, HTTPException, APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from web_app.database import get_db
from sqlalchemy.future import select
from web_app.schemas.contracts import ContractCreate, ContractResponse, ContractsModel
from web_app.services.auth_middleware import token_verification_dependency

router = APIRouter()


@router.get("/contracts", response_model=List[ContractResponse])
async def get_contracts(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    stmt = select(ContractsModel)
    result = await db.execute(stmt)
    contracts = result.scalars().all()
    return contracts


@router.get("/contracts/{contract_id}", response_model=ContractResponse)
async def get_contract_by_id(
    contract_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(ContractsModel).filter(ContractsModel.id == contract_id)
    )
    contract = result.scalar_one_or_none()
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Контракт не найден"
        )
    return contract


@router.post(
    "/contracts", response_model=ContractResponse, status_code=status.HTTP_201_CREATED
)
async def create_contract(
    contract_data: ContractCreate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    contract = ContractsModel(**contract_data.model_dump())
    db.add(contract)
    await db.commit()
    await db.refresh(contract)
    return contract


@router.patch("/contracts/{contract_id}", response_model=ContractResponse)
async def update_contract(
    contract_id: int,
    contract_data: ContractCreate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(ContractsModel).filter(ContractsModel.id == contract_id)
    )
    contract = result.scalar_one_or_none()
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Контракт не найден"
        )

    for key, value in contract_data.model_dump(exclude_unset=True).items():
        setattr(contract, key, value)

    await db.commit()
    await db.refresh(contract)
    return contract


@router.delete("/contracts/{contract_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contract(
    contract_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(ContractsModel).filter(ContractsModel.id == contract_id)
    )
    contract = result.scalar_one_or_none()
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Контракт не найден"
        )

    await db.delete(contract)
    await db.commit()
    return {"message": "Контракт успешно удален", "contract_id": contract_id}
