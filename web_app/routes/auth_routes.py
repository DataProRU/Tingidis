from fastapi import APIRouter, HTTPException, status
from datetime import timedelta
from sqlalchemy import select
from web_app.database import WebUser, async_session, TokenBlacklist
from web_app.schemas.users import UserLogin, UserCreate
from web_app.services.auth_service import (
    pwd_context,
    create_access_token,
    get_user_by_username,
    decode_token,
    add_token_to_blacklist,
)

router = APIRouter()


@router.post("/register")
async def register_user(user: UserCreate):
    # Проверка на отсутствие необходимых данных
    missing_fields = [
        field for field in ["username", "password", "role"] if not getattr(user, field)
    ]
    if missing_fields:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Отсутствуют обязательные поля: {', '.join(missing_fields)}",
        )

    async with async_session() as session:
        # Проверка, существует ли пользователь с таким логином
        if await get_user_by_username(user.username, session):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь уже существует",
            )

        # Хэшируем пароль
        hashed_password = pwd_context.hash(user.password)

        # Создаем нового пользователя с обязательными полями
        new_user = WebUser(
            username=user.username,
            password=hashed_password,
            role=user.role,
            last_name=user.username,  # Используем username как last_name по умолчанию
            first_name=user.username,  # Используем username как first_name по умолчанию
            full_name=user.username,  # Используем username как full_name
            email=f"{user.username}@example.com",  # Генерируем email
            login=user.username,  # Используем username как login
        )
        session.add(new_user)
        await session.commit()

        return {
            "access_token": create_access_token(
                {"sub": user.username, "role": user.role}
            ),
            "refresh_token": create_access_token(
                {"sub": user.username, "role": user.role}, timedelta(days=7)
            ),
            "user": {
                "username": new_user.username,
                "role": new_user.role,
                "id": new_user.id,
            },
        }


@router.post("/login")
async def login_user(user: UserLogin):
    async with async_session() as session:
        db_user = await get_user_by_username(user.username, session)
        if not db_user or not pwd_context.verify(user.password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверные учетные данные",
            )

        return {
            "access_token": create_access_token(
                {"sub": db_user.username, "role": db_user.role}
            ),
            "refresh_token": create_access_token(
                {"sub": db_user.username, "role": db_user.role}, timedelta(days=7)
            ),
            "user": {
                "username": db_user.username,
                "role": db_user.role,
                "id": db_user.id,
            },
        }


@router.post("/logout")
async def logout_user(access_token: str):
    payload = decode_token(access_token)
    async with async_session() as session:
        await add_token_to_blacklist(access_token, session)
    return {"message": "Успешно вышли из системы"}


@router.post("/refresh")
async def refresh_token(refresh_token: str):
    payload = decode_token(refresh_token)
    username, role = payload.get("sub"), payload.get("role")

    async with async_session() as session:
        blacklisted_token = await session.execute(
            select(TokenBlacklist).filter_by(token=refresh_token)
        )
        if blacklisted_token.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен обновлён и не является действительным",
            )

    return {"access_token": create_access_token({"sub": username, "role": role})}
