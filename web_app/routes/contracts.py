from fastapi import HTTPException, APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from web_app.database import get_db
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from web_app.models.contracts import Contracts
from web_app.schemas.contracts import (
    ContractsCreateResponse,
    ContractsResponse,
    ContractsGetResponse,
    ContractsUpdate,
)
from web_app.middlewares.auth_middleware import token_verification_dependency
from web_app.utils.logs import log_action

router = APIRouter()


# Endpoints
@router.get("/contracts", response_model=List[ContractsGetResponse])
async def get_contracts(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    stmt = select(Contracts).options(
        selectinload(Contracts.code_info),
        selectinload(Contracts.customer_info),
        selectinload(Contracts.executor_info),
        selectinload(Contracts.agreements),
    )
    result = await db.execute(stmt)
    contracts = result.scalars().all()

    response = []
    for contract in contracts:
        response.append(
            {
                "id": contract.id,
                "name": contract.name,
                "number": contract.number,
                "sign_date": contract.sign_date,
                "price": contract.price,
                "theme": contract.theme,
                "evolution": contract.evolution,
                "code": {
                    "id": contract.code_info.id,
                    "code": contract.code_info.code,
                    "name": contract.code_info.name,
                    "comment": contract.code_info.comment,
                },
                "customer": {
                    "id": contract.customer_info.id,
                    "form": contract.customer_info.form,
                    "name": contract.customer_info.name,
                    "address": contract.customer_info.address,
                    "inn": contract.customer_info.inn,
                    "notes": contract.customer_info.notes,
                },
                "executor": {
                    "id": contract.executor_info.id,
                    "first_name": contract.executor_info.first_name,
                    "last_name": contract.executor_info.last_name,
                    "father_name": contract.executor_info.father_name,
                    "full_name": contract.executor_info.full_name,
                    "position": contract.executor_info.position,
                    "phone": contract.executor_info.phone,
                    "email": contract.executor_info.email,
                    "telegram": contract.executor_info.telegram,
                    "birthday": contract.executor_info.birthday,
                    "category": contract.executor_info.category,
                    "specialization": contract.executor_info.specialization,
                    "username": contract.executor_info.username,
                    "notes": contract.executor_info.notes,
                    "role": contract.executor_info.role,
                    "notification": contract.executor_info.notification,
                },
                "agreements": [
                    {
                        "id": agreement.id,
                        "name": agreement.name,
                        "number": agreement.number,
                        "price": agreement.price,
                        "deadline": agreement.deadline,
                        "notes": agreement.notes,
                        "contract": agreement.contract,
                    }
                    for agreement in contract.agreements
                ],
            }
        )

    return response


@router.get(
    "/contracts/{contract_id}",
    response_model=ContractsGetResponse,
)
async def get_contract_by_id(
    contract_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(Contracts)
        .options(
            selectinload(Contracts.code_info),
            selectinload(Contracts.customer_info),
            selectinload(Contracts.executor_info),
            selectinload(Contracts.agreements),
        )
        .filter(Contracts.id == contract_id)
    )
    contract = result.scalar_one_or_none()
    if not contract:
        raise HTTPException(status_code=404, detail="Контракт не найден")
    return {
        "id": contract.id,
        "name": contract.name,
        "number": contract.number,
        "sign_date": contract.sign_date,
        "price": contract.price,
        "theme": contract.theme,
        "evolution": contract.evolution,
        "code": {
            "id": contract.code_info.id,
            "code": contract.code_info.code,
            "name": contract.code_info.name,
            "comment": contract.code_info.comment,
        },
        "customer": {
            "id": contract.customer_info.id,
            "form": contract.customer_info.form,
            "name": contract.customer_info.name,
            "address": contract.customer_info.address,
            "inn": contract.customer_info.inn,
            "notes": contract.customer_info.notes,
        },
        "executor": {
            "id": contract.executor_info.id,
            "first_name": contract.executor_info.first_name,
            "last_name": contract.executor_info.last_name,
            "father_name": contract.executor_info.father_name,
            "full_name": contract.executor_info.full_name,
            "position": contract.executor_info.position,
            "phone": contract.executor_info.phone,
            "email": contract.executor_info.email,
            "telegram": contract.executor_info.telegram,
            "birthday": contract.executor_info.birthday,
            "category": contract.executor_info.category,
            "specialization": contract.executor_info.specialization,
            "username": contract.executor_info.username,
            "notes": contract.executor_info.notes,
            "role": contract.executor_info.role,
        },
        "agreements": [
            {
                "id": agreement.id,
                "name": agreement.name,
                "number": agreement.number,
                "price": agreement.price,
                "deadline": agreement.deadline,
                "notes": agreement.notes,
                "contract": agreement.contract,
            }
            for agreement in contract.agreements
        ],
    }


@router.post(
    "/contracts",
    response_model=ContractsResponse,
    status_code=status.HTTP_201_CREATED,
)
@log_action("Создание контракта")
async def create_contract(
    contract_data: ContractsCreateResponse,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    contract = Contracts(**contract_data.dict())
    db.add(contract)
    await db.commit()
    await db.refresh(contract)
    return contract


@router.patch(
    "/contracts/{object_id}",
    response_model=ContractsGetResponse,
)
@log_action("Обновление контракта")
async def update_contract(
    object_id: int,
    object_data: ContractsUpdate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):

    result = await db.execute(
        select(Contracts)
        .options(
            selectinload(Contracts.code_info),
            selectinload(Contracts.customer_info),
            selectinload(Contracts.executor_info),
            selectinload(Contracts.agreements),
        )
        .filter(Contracts.id == object_id)
    )
    contract = result.scalar_one_or_none()
    if not contract:
        raise HTTPException(status_code=404, detail="Контракт не найден")

    for key, value in object_data.dict(exclude_unset=True).items():
        setattr(contract, key, value)

    await db.commit()
    await db.refresh(contract)

    return {
        "id": contract.id,
        "code": {
            "id": contract.code_info.id,
            "code": contract.code_info.code,
            "name": contract.code_info.name,
            "comment": contract.code_info.comment,
        },
        "name": contract.name,
        "number": contract.number,
        "sign_date": contract.sign_date,
        "price": contract.price,
        "theme": contract.theme,
        "evolution": contract.evolution,
        "customer": {
            "id": contract.customer_info.id,
            "form": contract.customer_info.form,
            "name": contract.customer_info.name,
            "address": contract.customer_info.address,
            "inn": contract.customer_info.inn,
            "notes": contract.customer_info.notes,
        },
        "executor": {
            "id": contract.executor_info.id,
            "first_name": contract.executor_info.first_name,
            "last_name": contract.executor_info.last_name,
            "father_name": contract.executor_info.father_name,
            "full_name": contract.executor_info.full_name,
            "position": contract.executor_info.position,
            "phone": contract.executor_info.phone,
            "email": contract.executor_info.email,
            "telegram": contract.executor_info.telegram,
            "birthday": contract.executor_info.birthday,
            "category": contract.executor_info.category,
            "specialization": contract.executor_info.specialization,
            "username": contract.executor_info.username,
            "notes": contract.executor_info.notes,
            "role": contract.executor_info.role,
        },
        "agreements": [
            {
                "id": agreement.id,
                "name": agreement.name,
                "number": agreement.number,
                "price": agreement.price,
                "deadline": agreement.deadline,
                "notes": agreement.notes,
                "contract": agreement.contract,
            }
            for agreement in contract.agreements
        ],
    }


@router.delete("/contracts/{object_id}", status_code=status.HTTP_204_NO_CONTENT)
@log_action("Удаление контракта")
async def delete_contract(
    object_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    # Проверка наличия объекта
    result = await db.execute(select(Contracts).filter(Contracts.id == object_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Контракт не найден")

    # Удаление объекта
    await db.delete(obj)
    await db.commit()
    return {
        "message": "Контракт успешно удален",
        "contract_id": object_id,
    }
