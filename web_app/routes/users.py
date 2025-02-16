import logging
from fastapi import APIRouter, Depends, status, HTTPException

from web_app.models.users import Users
from web_app.schemas.users import UserResponse, UserCreate, UserUpdate

from web_app.database import get_db
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from typing import List
from web_app.middlewares.auth_middleware import token_verification_dependency

from web_app.utils.logs import log_action

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="web_app/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/users", response_model=List[UserResponse])
async def get_users(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    stmt = select(Users)
    result = await db.execute(stmt)
    users = result.scalars().all()

    is_admin = user_data.get("role") == "admin"

    return [
        {**user.__dict__, "password": user.password if is_admin else None}
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

    # Удаление объекта
    await db.delete(user)
    await db.commit()
    return {"message": "Пользователь успешно удален", "user_id": object_id}
