from fastapi import HTTPException, APIRouter, Depends, status, Query
from typing import Annotated, Optional, List

from sqlalchemy import and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from web_app.database import get_db
from sqlalchemy.future import select

from web_app.models import Customers
from web_app.models.form_of_ownerships import FormOfOwnerships
from web_app.schemas.form_of_ownership import (
    FormOfOwnershipCreate,
    FormOfOwnershipResponse,
)
from web_app.middlewares.auth_middleware import token_verification_dependency
from web_app.utils.logs import log_action

router = APIRouter()


# Endpoints


@router.get("/form-of-ownership", response_model=list[FormOfOwnershipResponse])
async def get_form_of_ownerships(
    db: AsyncSession = Depends(get_db),
    id: Annotated[list[int] | None, Query()] = None,
    name: Annotated[list[str] | None, Query()] = None,
    user_data: dict = Depends(token_verification_dependency),
    sortBy: Optional[str] = None,
    sortDir: Optional[str] = "asc",
):
    stmt = select(FormOfOwnerships)

    filters = []

    if id:
        filters.append((FormOfOwnerships.id.in_(id)))
    if name:
        filters.append(or_(FormOfOwnerships.name.ilike(f"%{n}%") for n in name))

    if filters:
        stmt = stmt.where(and_(*filters))

    if sortBy:
        try:
            sort_column = getattr(FormOfOwnerships, sortBy)
            if sortDir.lower() == "desc":
                stmt = stmt.order_by(sort_column.desc())
            else:
                stmt = stmt.order_by(sort_column.asc())
        except AttributeError:
            raise HTTPException(status_code=404, detail="Поле не найдено")

    result = await db.execute(stmt)
    form_of_ownerships = result.scalars().all()

    return form_of_ownerships


@router.get(
    "/form-of-ownership/{form_of_ownership_id}", response_model=FormOfOwnershipResponse
)
async def get_form_of_ownership_by_id(
    form_of_ownership_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(FormOfOwnerships).filter(FormOfOwnerships.id == form_of_ownership_id)
    )
    form_of_ownership = result.scalar_one_or_none()
    if not form_of_ownership:
        raise HTTPException(status_code=404, detail="Форма собственности не найдена")
    return form_of_ownership


@router.post(
    "/form-of-ownership",
    response_model=FormOfOwnershipResponse,
    status_code=status.HTTP_201_CREATED,
)
@log_action("Создание формы собственности")
async def create_form_of_ownership(
    form_of_ownership_data: FormOfOwnershipCreate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    form_of_ownership = FormOfOwnerships(**form_of_ownership_data.dict())
    db.add(form_of_ownership)
    await db.commit()
    await db.refresh(form_of_ownership)
    return form_of_ownership


@router.patch(
    "/form-of-ownership/{form_of_ownership_id}", response_model=FormOfOwnershipResponse
)
@log_action("Обновление формы собственности")
async def update_form_of_ownership(
    form_of_ownership_id: int,
    object_data: FormOfOwnershipCreate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(FormOfOwnerships).filter(FormOfOwnerships.id == form_of_ownership_id)
    )
    form_of_ownership = result.scalar_one_or_none()
    if not form_of_ownership:
        raise HTTPException(status_code=404, detail="Форма собственности не найдена")

    for key, value in object_data.dict(exclude_unset=True).items():
        setattr(form_of_ownership, key, value)

    await db.commit()
    await db.refresh(form_of_ownership)
    return form_of_ownership


@router.delete("/form-of-ownership/{object_id}", status_code=status.HTTP_204_NO_CONTENT)
@log_action("Удаление формы собственности")
async def delete_form_of_ownership(
    object_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    # Проверка наличия объекта
    result = await db.execute(
        select(FormOfOwnerships).filter(FormOfOwnerships.id == object_id)
    )
    form_of_ownership = result.scalar_one_or_none()
    if not form_of_ownership:
        raise HTTPException(status_code=404, detail="Форма собственности не найдена")

    customers_exist = await db.execute(
        select(Customers).filter(Customers.form == object_id).limit(1)
    )
    if customers_exist.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Невозможно удалить форму собственности: существуют связанные заказчики. Удалите их сначала.",
        )

    # Удаление объекта
    await db.delete(form_of_ownership)
    await db.commit()
    return {
        "message": "Форма собственности успешно удалена",
        "form_of_ownership_id": object_id,
    }
