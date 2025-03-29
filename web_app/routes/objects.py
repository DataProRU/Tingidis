from fastapi import HTTPException, APIRouter, Depends, status, Query
from typing import Annotated, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from web_app.database import get_db
from sqlalchemy.future import select

from web_app.models import Contracts, Projects
from web_app.models.objects import Objects
from web_app.schemas.objects import ObjectCreate, ObjectResponse
from web_app.middlewares.auth_middleware import token_verification_dependency
from web_app.utils.logs import log_action
from sqlalchemy import exc, and_, or_

router = APIRouter()


# Endpoints


@router.get("/objects", response_model=list[ObjectResponse])
async def get_objects(
    db: AsyncSession = Depends(get_db),
    id: Annotated[list[int] | None, Query()] = None,
    code: Annotated[list[str] | None, Query()] = None,
    name: Annotated[list[str] | None, Query()] = None,
    comment: Annotated[list[str] | None, Query()] = None,
    user_data: dict = Depends(token_verification_dependency),
    sortBy: Optional[str] = None,
    sortDir: Optional[str] = "asc",
):
    stmt = select(Objects)

    filters = []

    if id:
        filters.append((Objects.id.in_(id)))
    if code:
        filters.append(or_(Objects.code.ilike(f"%{c}%") for c in code))
    if name:
        filters.append(or_(Objects.name.ilike(f"%{n}%") for n in name))
    if comment:
        filters.append(or_(Objects.comment.ilike(f"%{c}%") for c in comment))

    if filters:
        stmt = stmt.where(and_(*filters))

    if sortBy:
        try:
            sort_column = getattr(Objects, sortBy)
            if sortDir.lower() == "desc":
                stmt = stmt.order_by(sort_column.desc())
            else:
                stmt = stmt.order_by(sort_column.asc())
        except AttributeError:
            raise HTTPException(status_code=404, detail="Поле не найдено")

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
    # Проверка на уникальность поля code
    result = await db.execute(select(Objects).filter(Objects.code == object_data.code))
    existing_obj = result.scalar_one_or_none()
    if existing_obj:
        raise HTTPException(
            status_code=400, detail="Обьект с таким кодом уже существует"
        )

    obj = Objects(**object_data.dict())
    db.add(obj)
    try:
        await db.commit()
    except exc.IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail="Обьект с таким кодом уже существует"
        )
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

    # Проверка на уникальность поля code
    if object_data.code:
        result = await db.execute(
            select(Objects).filter(
                Objects.code == object_data.code, Objects.id != object_id
            )
        )
        existing_obj = result.scalar_one_or_none()
        if existing_obj:
            raise HTTPException(
                status_code=400, detail="Обьект с таким кодом уже существует"
            )

    for key, value in object_data.dict(exclude_unset=True).items():
        setattr(obj, key, value)

    try:
        await db.commit()
    except exc.IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail="Обьект с таким кодом уже существует"
        )
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

    contracts_exist = await db.execute(
        select(Contracts).filter(Contracts.code == object_id).limit(1)
    )
    if contracts_exist.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Невозможно удалить объект: существуют связанные контракты. Удалите их сначала.",
        )

    projects_exist = await db.execute(
        select(Projects).filter(Projects.object == object_id).limit(1)
    )
    if projects_exist.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Невозможно удалить объект: существуют связанные проекты. Удалите их сначала.",
        )

    # Удаление объекта
    await db.delete(obj)
    await db.commit()
    return {"message": "Объект успешно удален", "object_id": object_id}
