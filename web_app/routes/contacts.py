from fastapi import HTTPException, APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from web_app.database import get_db
from sqlalchemy.future import select
from web_app.models.contacts import Contacts
from web_app.schemas.contacts import (
    ContactResponse,
    ContactUpdate,
    ContactGetResponse,
)
from web_app.middlewares.auth_middleware import token_verification_dependency

from web_app.utils.logs import log_action

router = APIRouter()


# Endpoints
@router.get("/contacts", response_model=List[ContactGetResponse])
async def get_contacts(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    stmt = select(Contacts).options(selectinload(Contacts.customer_info))
    result = await db.execute(stmt)
    contacts = result.scalars().all()

    response = []
    for contact in contacts:
        response.append(
            {
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
        )

    return response


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
