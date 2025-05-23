from fastapi import HTTPException, APIRouter, Depends, status, Query
from typing import Annotated, List, Optional

from sqlalchemy import and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from web_app.database import get_db
from sqlalchemy.future import select

from web_app.models import Customers
from web_app.models.contacts import Contacts
from web_app.schemas.contacts import (
    ContactResponse,
    ContactUpdate,
    ContactGetResponse,
)
from web_app.middlewares.auth_middleware import token_verification_dependency

from web_app.utils.logs import log_action

router = APIRouter()


@router.get("/contacts", response_model=list[ContactGetResponse])
async def get_contacts(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
    id: Annotated[list[int] | None, Query()] = None,
    first_name: Annotated[list[str] | None, Query()] = None,
    last_name: Annotated[list[str] | None, Query()] = None,
    father_name: Annotated[list[str] | None, Query()] = None,
    phone: Annotated[list[str] | None, Query()] = None,
    email: Annotated[list[str] | None, Query()] = None,
    position: Annotated[list[str] | None, Query()] = None,
    customer: Annotated[list[str] | None, Query()] = None,
    sortBy: Optional[str] = None,  # поле для сортировки
    sortDir: Optional[str] = "asc",  # направление сортировки
):
    join_customers = sortBy == "customer" or bool(customer)

    if join_customers:
        stmt = (
            select(Contacts)
            .join(Contacts.customer_info)
            .options(selectinload(Contacts.customer_info))
        )
    else:
        stmt = select(Contacts).options(selectinload(Contacts.customer_info))

    filters = []

    if id:
        filters.append((Contacts.id.in_(id)))
    if first_name:
        filters.append(or_(Contacts.first_name.ilike(f"%{n}%") for n in first_name))
    if last_name:
        filters.append(or_(Contacts.last_name.ilike(f"%{n}%") for n in last_name))
    if father_name:
        filters.append(or_(Contacts.father_name.ilike(f"%{n}%") for n in father_name))
    if phone:
        filters.append(or_(Contacts.phone.ilike(f"%{n}%") for n in phone))
    if email:
        filters.append(or_(Contacts.email.ilike(f"%{n}%") for n in email))
    if position:
        filters.append(or_(Contacts.position.ilike(f"%{n}%") for n in position))

    if customer:
        if not join_customers:
            stmt = stmt.join(Contacts.customer_info)
        filters.append(or_(Customers.name.ilike(f"%{n}%") for n in customer))

    if filters:
        stmt = stmt.where(and_(*filters))

    if sortBy:
        if sortBy == "customer":
            if not join_customers:
                stmt = stmt.join(Contacts.customer_info)
            sort_column = Customers.name
        else:
            try:
                sort_column = getattr(Contacts, sortBy)
            except AttributeError:
                raise HTTPException(
                    status_code=404, detail="Поле для сортировки не найдено"
                )

        # Применяем направление сортировки
        if sortDir.lower() == "desc":
            stmt = stmt.order_by(sort_column.desc())
        else:
            stmt = stmt.order_by(sort_column.asc())

    result = await db.execute(stmt)
    contacts = result.scalars().all()

    return [
        {
            "id": contact.id,
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "father_name": contact.father_name,
            "phone": contact.phone,
            "email": contact.email,
            "position": contact.position,
            "customer": (
                {
                    "id": contact.customer_info.id,
                    "form": contact.customer_info.form,
                    "name": contact.customer_info.name,
                    "address": contact.customer_info.address,
                    "inn": contact.customer_info.inn,
                    "notes": contact.customer_info.notes,
                }
                if contact.customer_info
                else None
            ),
        }
        for contact in contacts
    ]


@router.get("/contacts/{contact_id}", response_model=ContactGetResponse)
async def get_contact_by_id(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(Contacts)
        .options(selectinload(Contacts.customer_info))
        .filter(Contacts.id == contact_id)
    )
    contact = result.scalar_one_or_none()

    if not contact:
        raise HTTPException(status_code=404, detail="Контакт не найден")

    return {
        "id": contact.id,
        "first_name": contact.first_name,
        "last_name": contact.last_name,
        "father_name": contact.father_name,
        "phone": contact.phone,
        "email": contact.email,
        "position": contact.position,
        "customer": {
            "id": contact.customer_info.id,
            "form": contact.customer_info.form,
            "name": contact.customer_info.name,
            "address": contact.customer_info.address,
            "inn": contact.customer_info.inn,
            "notes": contact.customer_info.notes,
        },
    }


@router.post(
    "/contacts",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
)
@log_action("Создание контакта")
async def create_contact(
    contact_data: ContactResponse,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    obj = Contacts(**contact_data.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.patch("/contacts/{contact_id}", response_model=ContactGetResponse)
@log_action("Обновление контакта")
async def update_contact(
    contact_id: int,
    object_data: ContactUpdate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(Contacts)
        .options(selectinload(Contacts.customer_info))
        .filter(Contacts.id == contact_id)
    )
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Контакт не найден")

    for key, value in object_data.dict(exclude_unset=True).items():
        setattr(obj, key, value)

    await db.commit()
    await db.refresh(obj)
    return {
        "id": obj.id,
        "first_name": obj.first_name,
        "last_name": obj.last_name,
        "father_name": obj.father_name,
        "phone": obj.phone,
        "email": obj.email,
        "position": obj.position,
        "customer": {
            "id": obj.customer_info.id,
            "form": obj.customer_info.form,
            "name": obj.customer_info.name,
            "address": obj.customer_info.address,
            "inn": obj.customer_info.inn,
            "notes": obj.customer_info.notes,
        },
    }


@router.delete("/contacts/{object_id}", status_code=status.HTTP_204_NO_CONTENT)
@log_action("Удаление контакта")
async def delete_contact(
    object_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    # Проверка наличия объекта
    result = await db.execute(select(Contacts).filter(Contacts.id == object_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Контакт не найден")

    # Удаление объекта
    await db.delete(obj)
    await db.commit()
    return {
        "message": "Контакт успешно удален",
        "contact_id": object_id,
    }
