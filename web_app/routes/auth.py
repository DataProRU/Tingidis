import os

from fastapi import APIRouter, HTTPException, Response, Request, Depends, status
from passlib.context import CryptContext
from datetime import timedelta, date

from sqlalchemy.ext.asyncio import AsyncSession

from web_app.database import async_session, get_db
from web_app.models.users import Users
from web_app.models.token import Tokens
from sqlalchemy import select
from web_app.schemas.users import UserCreate, UserLogin
from web_app.services.auth import (
    create_token,
    save_token,
    validate_refresh_token,
    remove_token,
)

from dotenv import load_dotenv

router = APIRouter()

# Настройка для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Загружаем переменные окружения
load_dotenv()


# Секретный ключ и алгоритм для JWT
SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_KEY = os.getenv("REFRESH_KEY")
ALGORITHM = os.getenv("ALGORITHM")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserCreate, response: Response, db: AsyncSession = Depends(get_db)
):
    # Создаем сессию базы данных вручную
    result = await db.execute(select(Users).filter_by(username=user.username))

    existing_user = (
        result.scalar_one_or_none()
    )  # Вернет None, если пользователь не найден
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь существует")

    # Хэшируем пароль
    hashed_password = pwd_context.hash(user.password)

    # Создаем нового пользователя
    new_user = Users(
        username=user.username,
        password=hashed_password,
        role=user.role,
    )
    db.add(new_user)
    await db.commit()

    # Создаем токены с ролью пользователя в payload
    access_token = create_token(
        data={"sub": user.username, "role": user.role},
        key=SECRET_KEY,
        algoritm=ALGORITHM,
    )
    refresh_token = create_token(
        data={"sub": user.username, "role": user.role},
        key=REFRESH_KEY,
        algoritm=ALGORITHM,
        expires_delta=timedelta(days=7),
    )

    await save_token(new_user.id, refresh_token, db)

    response.set_cookie(
        key="refresh_token", value=refresh_token, httponly=True, max_age=604800
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "username": new_user.username,
            "role": new_user.role,
            "id": new_user.id,
        },
    }


@router.post("/login")
async def login_user(
    user: UserLogin, response: Response, db: AsyncSession = Depends(get_db)
):
    # Создаем сессию базы данных вручную
    # Ищем пользователя в базе данных
    result = await db.execute(select(Users).filter_by(username=user.username))
    existing_user = (
        result.scalar_one_or_none()
    )  # Вернет None, если пользователь не найден
    if not existing_user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    # Проверяем, совпадает ли введенный пароль с хэшированным
    if not pwd_context.verify(user.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    # Создаем токены с ролью пользователя в payload
    access_token = create_token(
        data={"sub": existing_user.username, "role": existing_user.role},
        key=SECRET_KEY,
        algoritm=ALGORITHM,
    )
    refresh_token = create_token(
        data={"sub": existing_user.username, "role": existing_user.role},
        key=REFRESH_KEY,
        algoritm=ALGORITHM,
        expires_delta=timedelta(days=7),
    )
    await save_token(existing_user.id, refresh_token, db)
    response.set_cookie(
        key="refresh_token", value=refresh_token, httponly=True, max_age=604800
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "username": existing_user.username,
            "role": existing_user.role,
            "id": existing_user.id,
        },
    }


@router.get("/refresh")
async def refresh_token(
    request: Request, response: Response, db: AsyncSession = Depends(get_db)
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    # Декодируем refresh token из cookies
    user_data = validate_refresh_token(refresh_token, REFRESH_KEY, ALGORITHM)
    # Ищем токен в бд
    token_query = await db.execute(
        select(Tokens).filter_by(refresh_token=refresh_token)
    )
    token_data = token_query.scalar_one_or_none()
    if not user_data or not token_data:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")

    user_id = token_data.user_id

    user_query = await db.execute(select(Users).filter_by(id=user_id))
    user = user_query.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    access_token = create_token(
        data={"sub": user.username, "role": user.role},
        key=SECRET_KEY,
        algoritm=ALGORITHM,
    )
    refresh_token = create_token(
        data={"sub": user.username, "role": user.role},
        key=REFRESH_KEY,
        algoritm=ALGORITHM,
        expires_delta=timedelta(days=7),
    )
    await save_token(user.id, refresh_token, db)
    response.set_cookie(
        key="refresh_token", value=refresh_token, httponly=True, max_age=604800
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "username": user.username,
            "role": user.role,
            "id": user.id,
        },
    }


@router.post("/logout")
async def logout_user(
    request: Request, response: Response, db: AsyncSession = Depends(get_db)
):
    refresh_token = request.cookies.get("refresh_token")

    if refresh_token:
        await remove_token(refresh_token, db)

    # Delete the refresh_token cookie
    response.delete_cookie(key="refresh_token")

    # Return the refresh_token in the JSON response
    return {"refresh_token": refresh_token}


@router.get("/tokens", response_model=None)
async def get_all_tokens():
    async with async_session() as session:
        # Query to get all tokens
        result = await session.execute(select(Tokens))
        tokens = result.scalars().all()  # Get all token records

    return tokens
