from datetime import date

from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy import or_, and_

from web_app.models import Contracts, Projects
from web_app.models.users import Users
from web_app.schemas.users import UserResponse, UserCreate, UserUpdate

from web_app.database import get_db
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from typing import Annotated, Optional, List
from web_app.middlewares.auth_middleware import token_verification_dependency

from web_app.utils.logs import log_action

router = APIRouter()
templates = Jinja2Templates(directory="web_app/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/users", response_model=list[UserResponse])
async def get_users(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
    id: Annotated[list[int] | None, Query()] = None,
    username: Annotated[list[str] | None, Query()] = None,
    full_name: Annotated[list[str] | None, Query()] = None,
    first_name: Annotated[list[str] | None, Query()] = None,
    last_name: Annotated[list[str] | None, Query()] = None,
    father_name: Annotated[list[str] | None, Query()] = None,
    email: Annotated[list[str] | None, Query()] = None,
    phone: Annotated[list[str] | None, Query()] = None,
    position: Annotated[list[str] | None, Query()] = None,
    role: Annotated[list[str] | None, Query()] = None,
    specialization: Annotated[list[str] | None, Query()] = None,
    category: Annotated[list[str] | None, Query()] = None,
    birthday: Annotated[list[date] | None, Query()] = None,
    password: Annotated[list[str] | None, Query()] = None,
    telegram: Annotated[list[str] | None, Query()] = None,
    notes: Annotated[list[str] | None, Query()] = None,
    sortBy: Optional[str] = None,
    sortDir: Optional[str] = "asc",
):
    stmt = select(Users)

    filters = []

    if id:
        filters.append((Users.id.in_(id)))
    if username:
        filters.append(or_(Users.username.ilike(f"%{u}%") for u in username))
    if full_name:
        filters.append(
            or_(
                or_(
                    Users.full_name.ilike(f"%{name}%"),
                    Users.first_name.ilike(f"%{name}%"),
                    Users.last_name.ilike(f"%{name}%"),
                )
                for name in full_name
            )
        )
    if first_name:
        filters.append(or_(Users.first_name.ilike(f"%{n}%") for n in first_name))
    if father_name:
        filters.append(or_(Users.father_name.ilike(f"%{n}%") for n in father_name))
    if last_name:
        filters.append(or_(Users.last_name.ilike(f"%{n}%") for n in last_name))
    if email:
        filters.append(or_(Users.email.ilike(f"%{e}%") for e in email))
    if phone:
        filters.append(or_(Users.phone.ilike(f"%{p}%") for p in phone))
    if position:
        filters.append(or_(Users.position.ilike(f"%{p}%") for p in position))
    if telegram:
        filters.append(or_(Users.telegram.ilike(f"%{p}%") for p in telegram))
    if role:
        filters.append(or_(Users.role.ilike(f"%{p}%") for p in role))
    if specialization:
        filters.append(
            or_(Users.specialization.ilike(f"%{s}%") for s in specialization)
        )
    if category:
        filters.append(or_(Users.category.ilike(f"%{c}%") for c in category))
    if password:
        filters.append(or_(Users.password.ilike(f"%{c}%") for c in password))
    if notes:
        filters.append(or_(Users.notes.ilike(f"%{c}%") for c in notes))

    if birthday:
        filters.append(Users.birthday.in_(birthday))

    if filters:
        stmt = stmt.where(and_(*filters))

    if sortBy:
        try:
            sort_column = getattr(Users, sortBy)
            if sortDir.lower() == "desc":
                stmt = stmt.order_by(sort_column.desc())
            else:
                stmt = stmt.order_by(sort_column.asc())
        except AttributeError:
            raise HTTPException(status_code=404, detail="Поле не найдено")

    result = await db.execute(stmt)
    users = result.scalars().all()

    is_admin = user_data.get("role") == "admin"

    return [
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "father_name": user.father_name,
            "full_name": user.full_name,
            "position": user.position,
            "phone": user.phone,
            "email": user.email,
            "telegram": user.telegram,
            "birthday": user.birthday,
            "category": user.category,
            "specialization": user.specialization,
            "username": user.username,
            "password": user.password if is_admin else None,
            "notes": user.notes,
            "role": user.role,
            "notification": user.notification,
        }
        for user in users
    ]


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(select(Users).filter(Users.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    is_admin = user_data.get("role") == "admin"

    # Формируем ответ в зависимости от роли
    return {**user.__dict__, "password": user.password if is_admin else None}


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@log_action("Создание пользователя")
async def create_user(
    user_data_create: UserCreate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    if user_data.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Отсутствует доступ к запросу",
        )

    # Проверяем, существует ли пользователь с таким username
    existing_user = await db.execute(
        select(Users).where(Users.username == user_data_create.username)
    )
    if existing_user.scalar():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким username уже существует",
        )

    # Хэшируем пароль перед созданием пользователя
    hashed_password = pwd_context.hash(user_data_create.password)
    user_data_create.password = hashed_password
    user_data_create.full_name = (
        f"{user_data_create.last_name} {user_data_create.first_name}"
    )

    # Создаем нового пользователя
    user = Users(**user_data_create.dict())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.patch("/users/{user_id}", response_model=UserUpdate)
@log_action("Обновление пользователя")
async def update_user(
    user_id: int,
    web_user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    if user_data.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Отсутствует доступ к запросу",
        )

    result = await db.execute(select(Users).filter(Users.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    update_data = web_user_data.dict(exclude_unset=True)

    # Проверка на уникальность логина, если он был передан
    if "username" in update_data and update_data["username"]:
        existing_user = await db.execute(
            select(Users).filter(
                Users.username == update_data["username"], Users.id != user_id
            )
        )
        if existing_user.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким логином уже существует",
            )

    for key, value in update_data.items():
        if key == "password" and value:  # Если передан пароль, хэшируем его
            hashed_password = pwd_context.hash(value)
            setattr(user, key, hashed_password)
        else:
            setattr(user, key, value)

    if (
        "first_name" in update_data
        or "last_name" in update_data
        or "father_name" in update_data
    ):
        first_name = update_data.get("first_name", user.first_name)
        last_name = update_data.get("last_name", user.last_name)
        father_name = update_data.get("father_name", user.father_name)

        full_name_parts = [last_name]
        full_name_parts.append(first_name)
        if father_name:
            full_name_parts.append(father_name)

        user.full_name = " ".join(full_name_parts)

    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/users/{object_id}", status_code=status.HTTP_204_NO_CONTENT)
@log_action("Удаление пользователя")
async def delete_user(
    object_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    if user_data.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Отсутствует доступ к запросу",
        )
    # Проверка наличия объекта
    result = await db.execute(select(Users).filter(Users.id == object_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    contracts_exist = await db.execute(
        select(Contracts).filter(Contracts.executor == object_id).limit(1)
    )
    if contracts_exist.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Невозможно удалить пользователя: существуют связанные договоры. Удалите их сначала.",
        )

    projects_exist = await db.execute(
        select(Projects).filter(Projects.main_executor == object_id).limit(1)
    )
    if projects_exist.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Невозможно удалить пользователя: существуют связанные проекты. Удалите их сначала.",
        )

    # Удаление объекта
    await db.delete(user)
    await db.commit()
    return {"message": "Пользователь успешно удален", "user_id": object_id}
