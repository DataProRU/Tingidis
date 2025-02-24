from fastapi import HTTPException, APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from web_app.database import get_db
from sqlalchemy.future import select
from web_app.models.objects import Objects
from web_app.schemas.objects import ObjectCreate, ObjectResponse
from web_app.middlewares.auth_middleware import token_verification_dependency
from web_app.utils.logs import log_action

router = APIRouter()


# Endpoints
@router.get("/objects", response_model=List[ObjectResponse])
async def get_objects(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    stmt = select(Objects)
    result = await db.execute(stmt)
    objects = result.scalars().all()
    return objects


@router.get("/objects/{object_id}", response_model=ObjectResponse)
async def get_object_by_id(
    object_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(select(Objects).filter(Objects.id == object_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Обьект не найден")
    return obj


@router.post(
    "/objects", response_model=ObjectResponse, status_code=status.HTTP_201_CREATED
)
@log_action("Создание объекта")
async def create_object(
    object_data: ObjectCreate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    obj = Objects(**object_data.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.patch("/objects/{object_id}", response_model=ObjectResponse)
@log_action("Обновление объекта")
async def update_object(
    object_id: int,
    object_data: ObjectCreate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(select(Objects).filter(Objects.id == object_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Обьект не найден")

    for key, value in object_data.dict(exclude_unset=True).items():
        setattr(obj, key, value)

    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/objects/{object_id}", status_code=status.HTTP_204_NO_CONTENT)
@log_action("Удаление объекта")
async def delete_object(
    object_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    # Проверка наличия объекта
    result = await db.execute(select(Objects).filter(Objects.id == object_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Обьект не найден")

    # Удаление объекта
    await db.delete(obj)
    await db.commit()
    return {"message": "Объект успешно удален", "object_id": object_id}
