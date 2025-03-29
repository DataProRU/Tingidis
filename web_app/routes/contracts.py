from datetime import datetime, date

from fastapi import HTTPException, APIRouter, Depends, status, Query
from typing import Annotated, Optional, List

from sqlalchemy import or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from web_app.database import get_db
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from web_app.models import Objects, Customers, Users, Agreements, Projects
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


@router.get("/contracts", response_model=list[ContractsGetResponse])
async def get_contracts(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
    id: Annotated[list[int] | None, Query()] = None,
    name: Annotated[list[str] | None, Query()] = None,
    number: Annotated[list[str] | None, Query()] = None,
    sign_date: Annotated[list[date] | None, Query()] = None,
    price: Annotated[list[float] | None, Query()] = None,
    theme: Annotated[list[str] | None, Query()] = None,
    evolution: Annotated[list[str] | None, Query()] = None,
    code: Annotated[list[str] | None, Query()] = None,
    customer: Annotated[list[str] | None, Query()] = None,
    executor: Annotated[list[str] | None, Query()] = None,
    sortBy: Optional[str] = None,  # поле для сортировки
    sortDir: Optional[str] = "asc",  # направление сортировки
):
    stmt = select(Contracts).options(
        selectinload(Contracts.code_info),
        selectinload(Contracts.customer_info),
        selectinload(Contracts.executor_info),
        selectinload(Contracts.agreements),
    )

    filters = []

    if id:
        filters.append((Contracts.id.in_(id)))
    if name:
        filters.append(or_(Contracts.name.ilike(f"%{n}%") for n in name))
    if number:
        filters.append(or_(Contracts.number.ilike(f"%{n}%") for n in number))
    if sign_date:
        filters.append(Contracts.sign_date.in_(sign_date))
    if price is not None:
        filters.append(Contracts.price.in_(price))
    if theme:
        filters.append(or_(Contracts.theme.ilike(f"%{t}%") for t in theme))
    if evolution:
        filters.append(or_(Contracts.evolution.ilike(f"%{e}%") for e in evolution))

    if code:
        stmt = stmt.join(Contracts.code_info)
        filters.append(or_(Objects.code.ilike(f"%{c}%") for c in code))

    if customer:
        stmt = stmt.join(Contracts.customer_info)
        filters.append(or_(Customers.name.ilike(f"%{n}%") for n in customer))

    if executor:
        stmt = stmt.join(Contracts.executor_info)
        filters.append(
            or_(
                Users.full_name.ilike(f"%{name}%"),
                Users.first_name.ilike(f"%{name}%"),
                Users.last_name.ilike(f"%{name}%"),
            )
            for name in executor
        )

    if filters:
        stmt = stmt.where(and_(*filters))

    if sortBy:
        try:
            sort_column = getattr(Contracts, sortBy)
            if sortDir.lower() == "desc":
                stmt = stmt.order_by(sort_column.desc())
            else:
                stmt = stmt.order_by(sort_column.asc())
        except AttributeError:
            raise HTTPException(status_code=404, detail="Поле не найдено")

    result = await db.execute(stmt)
    contracts = result.scalars().all()

    return [
        {
            "id": contract.id,
            "name": contract.name,
            "number": contract.number,
            "sign_date": contract.sign_date,
            "price": contract.price,
            "theme": contract.theme,
            "evolution": contract.evolution,
            "code": (
                {
                    "id": contract.code_info.id,
                    "code": contract.code_info.code,
                    "name": contract.code_info.name,
                    "comment": contract.code_info.comment,
                }
                if contract.code_info
                else None
            ),
            "customer": (
                {
                    "id": contract.customer_info.id,
                    "form": contract.customer_info.form,
                    "name": contract.customer_info.name,
                    "address": contract.customer_info.address,
                    "inn": contract.customer_info.inn,
                    "notes": contract.customer_info.notes,
                }
                if contract.customer_info
                else None
            ),
            "executor": (
                {
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
                }
                if contract.executor_info
                else None
            ),
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
        for contract in contracts
    ]


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
    contract_dict = contract_data.dict()
    contract_dict["evolution"] = f'1. {(datetime.now()).strftime("%d.%m.%Y %H:%M:%S")}'

    contract = Contracts(**contract_dict)
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

    current_number = int(contract.evolution.split(".")[0].strip())
    new_number = current_number + 1

    current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    contract.evolution = f"{new_number}. {current_time}"

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

    projects_exist = await db.execute(
        select(Projects).filter(Projects.contract == object_id).limit(1)
    )
    if projects_exist.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Невозможно удалить контракт: существуют связанные проекты. Удалите их сначала.",
        )

    agreements_exist = await db.execute(
        select(Agreements).filter(Agreements.contract == object_id).limit(1)
    )
    if agreements_exist.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Невозможно удалить контракт: существуют связанные доп. соглашения. Удалите их сначала.",
        )

    # Удаление объекта
    await db.delete(obj)
    await db.commit()
    return {
        "message": "Контракт успешно удален",
        "contract_id": object_id,
    }
