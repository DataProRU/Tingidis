from fastapi import HTTPException, APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from web_app.database import get_db
from sqlalchemy.future import select
from web_app.models.form_of_ownerships import FormOfOwnerships
from web_app.schemas.form_of_ownership import (
    FormOfOwnershipCreate,
    FormOfOwnershipResponse,
)
from web_app.middlewares.auth_middleware import token_verification_dependency
from web_app.utils.logs import log_action

router = APIRouter()


# Endpoints
@router.get("/form-of-ownership", response_model=List[FormOfOwnershipResponse])
async def get_form_of_ownerships(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    stmt = select(FormOfOwnerships)
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

    # Удаление объекта
    await db.delete(form_of_ownership)
    await db.commit()
    return {
        "message": "Форма собственности успешно удалена",
        "form_of_ownership_id": object_id,
    }
