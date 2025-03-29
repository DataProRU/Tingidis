from fastapi import HTTPException, APIRouter, Depends, status, Query
from typing import Annotated, Optional, List

from sqlalchemy import and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from web_app.database import get_db
from sqlalchemy.future import select

from web_app.models import FormOfOwnerships, Contracts
from web_app.models.contacts import Contacts
from web_app.models.customers import Customers
from web_app.schemas.customers import (
    CustomerUpdate,
    CustomerResponse,
    CustomerGetResponse,
    CustomerCreateResponse,
)
from web_app.middlewares.auth_middleware import token_verification_dependency
from web_app.utils.logs import log_action

router = APIRouter()


# Endpoints


@router.get("/customers", response_model=list[CustomerGetResponse])
async def get_customers(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
    id: Annotated[list[int] | None, Query()] = None,
    name: Annotated[list[str] | None, Query()] = None,
    address: Annotated[list[str] | None, Query()] = None,
    inn: Annotated[list[str] | None, Query()] = None,
    notes: Annotated[list[str] | None, Query()] = None,
    form: Annotated[list[str] | None, Query()] = None,
    sortBy: Optional[str] = None,  # поле для сортировки
    sortDir: Optional[str] = "asc",  # направление сортировки
):
    stmt = select(Customers).options(
        selectinload(Customers.form_of_ownership), selectinload(Customers.contacts)
    )

    filters = []

    if id:
        filters.append((Contracts.id.in_(id)))
    if name:
        filters.append(or_(Customers.name.ilike(f"%{n}%") for n in name))
    if address:
        filters.append(or_(Customers.address.ilike(f"%{a}%") for a in address))
    if inn:
        filters.append(or_(Customers.inn.ilike(f"%{i}%") for i in inn))
    if notes:
        filters.append(or_(Customers.notes.ilike(f"%{n}%") for n in notes))
    if form:
        stmt = stmt.join(Customers.form_of_ownership)
        filters.append(or_(FormOfOwnerships.name.ilike(f"%{n}%") for n in form))

    if filters:
        stmt = stmt.where(and_(*filters))

    if sortBy:
        try:
            if "." in sortBy:  # Если сортировка по связанному полю
                related_model, field_name = sortBy.split(".")
                related_column = getattr(getattr(Customers, related_model), field_name)
                sort_column = related_column
            else:
                sort_column = getattr(Customers, sortBy)

            if sortDir.lower() == "desc":
                stmt = stmt.order_by(sort_column.desc())
            else:
                stmt = stmt.order_by(sort_column.asc())
        except AttributeError:
            raise HTTPException(status_code=404, detail=f"Поле '{sortBy}' не найдено")

    result = await db.execute(stmt)
    customers = result.scalars().all()

    return [
        {
            "id": customer.id,
            "form": (
                {
                    "id": customer.form_of_ownership.id,
                    "name": customer.form_of_ownership.name,
                }
                if customer.form_of_ownership
                else None
            ),
            "name": customer.name,
            "address": customer.address,
            "inn": customer.inn,
            "notes": customer.notes,
            "contacts": [
                {
                    "id": contact.id,
                    "first_name": contact.first_name,
                    "last_name": contact.last_name,
                    "father_name": contact.father_name,
                    "phone": contact.phone,
                    "email": contact.email,
                    "position": contact.position,
                    "customer": contact.customer,
                }
                for contact in customer.contacts
            ],
        }
        for customer in customers
    ]


@router.get("/customers/{customer_id}", response_model=CustomerGetResponse)
async def get_customer_by_id(
    customer_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(Customers)
        .options(
            selectinload(Customers.form_of_ownership), selectinload(Customers.contacts)
        )
        .filter(Customers.id == customer_id)
    )
    customer = result.scalar_one_or_none()

    if not customer:
        raise HTTPException(status_code=404, detail="Клиент не найден")

    return {
        "id": customer.id,
        "form": {
            "id": customer.form_of_ownership.id,
            "name": customer.form_of_ownership.name,
        },
        "name": customer.name,
        "address": customer.address,
        "inn": customer.inn,
        "notes": customer.notes,
        "contacts": [
            {
                "id": contact.id,
                "first_name": contact.first_name,
                "last_name": contact.last_name,
                "father_name": contact.father_name,
                "phone": contact.phone,
                "email": contact.email,
                "position": contact.position,
                "customer": contact.customer,
            }
            for contact in customer.contacts
        ],
    }


@router.post(
    "/customers",
    response_model=CustomerCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
@log_action("Создание заказчика")
async def create_customer(
    customer_data: CustomerCreateResponse,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    customer = Customers(
        form=customer_data.form,
        name=customer_data.name,
        address=customer_data.address,
        inn=customer_data.inn,
        notes=customer_data.notes,
    )

    db.add(customer)
    await db.commit()
    await db.refresh(customer)

    if customer_data.contacts:
        for contact_data in customer_data.contacts:
            contact = Contacts(
                first_name=contact_data.first_name,
                last_name=contact_data.last_name,
                father_name=contact_data.father_name,
                phone=contact_data.phone,
                email=contact_data.email,
                position=contact_data.position,
                customer=customer.id,
            )
            db.add(contact)

        await db.commit()

    await db.refresh(customer)

    return {
        "id": customer.id,
        "form": customer.form,
        "name": customer.name,
        "address": customer.address,
        "inn": customer.inn,
        "notes": customer.notes,
        "contacts": customer_data.contacts,
    }


@router.patch("/customers/{customer_id}", response_model=CustomerGetResponse)
@log_action("Обновление заказчика")
async def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(Customers)
        .options(
            selectinload(Customers.form_of_ownership), selectinload(Customers.contacts)
        )
        .filter(Customers.id == customer_id)
    )
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Клиент не найден")

    for key, value in customer_data.dict(exclude_unset=True).items():
        setattr(customer, key, value)

    await db.commit()
    await db.refresh(customer)
    return {
        "id": customer.id,
        "form": {
            "id": customer.form_of_ownership.id,
            "name": customer.form_of_ownership.name,
        },
        "name": customer.name,
        "address": customer.address,
        "inn": customer.inn,
        "notes": customer.notes,
        "contacts": [
            {
                "id": contact.id,
                "first_name": contact.first_name,
                "last_name": contact.last_name,
                "father_name": contact.father_name,
                "phone": contact.phone,
                "email": contact.email,
                "position": contact.position,
                "customer": contact.customer,
            }
            for contact in customer.contacts
        ],
    }


@router.delete("/customers/{object_id}", status_code=status.HTTP_204_NO_CONTENT)
@log_action("Удаление заказчика")
async def delete_customer(
    object_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    # Проверка наличия объекта
    result = await db.execute(select(Customers).filter(Customers.id == object_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Клиент не найден")

    contacts_exist = await db.execute(
        select(Contacts).filter(Contacts.customer == object_id).limit(1)
    )
    if contacts_exist.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Невозможно удалить заказчика: существуют связанные контакты. Удалите их сначала.",
        )

    contracts_exist = await db.execute(
        select(Contracts).filter(Contracts.customer == object_id).limit(1)
    )
    if contracts_exist.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Невозможно удалить заказчика: существуют связанные договоры. Удалите их сначала.",
        )

    # Удаление объекта
    await db.delete(obj)
    await db.commit()
    return {"message": "Клиент успешно удален", "customer_id": object_id}
