from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from web_app.database import WebUser, async_session, TokenSchema
from sqlalchemy import select
from fastapi import Response, Request


router = APIRouter()

# Настройка для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Секретный ключ и алгоритм для JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# Модель запроса для регистрации
class UserCreate(BaseModel):
    username: str
    password: str
    role: str

# Модель запроса для входа
class UserLogin(BaseModel):
    username: str
    password: str

# Функция для создания токенов
def create_tokens(data: dict, expires_delta: timedelta = timedelta(minutes=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def save_token(user_id, refresh_token):
    async with async_session() as session:
        async with session.begin():
            # Query for the existing token
            token_query = await session.execute(
                select(TokenSchema).filter_by(user_id=user_id)
            )
            existing_token = token_query.scalar_one_or_none()

            if existing_token:
                # Update the existing token's refresh_token
                existing_token.refresh_token = refresh_token
            else:
                # Create a new TokenSchema instance if no existing token is found
                new_token = TokenSchema(user_id=user_id, refresh_token=refresh_token)
                session.add(new_token)

        # Commit the transaction
        await session.commit()


async def remove_token(refresh_token):
    async with async_session() as session:
        async with session.begin():
            # Query for the token to be deleted
            token_query = await session.execute(
                select(TokenSchema).filter_by(refresh_token=refresh_token)
            )
            token_to_delete = token_query.scalar_one_or_none()

            if token_to_delete:
                # Delete the token if it exists
                await session.delete(token_to_delete)

        # Commit the transaction
        await session.commit()


def validate_access_token(access_token):
    try:
        user_data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        return user_data
    except Exception as e:
        return None


def validate_refresh_token(refresh_token):
    try:
        user_data = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        return user_data
    except Exception as e:
        return None

@router.post("/register")
async def register_user(user: UserCreate, response: Response):
    # Создаем сессию базы данных вручную
    async with async_session() as session:
        # Проверяем, существует ли пользователь с таким логином
        result = await session.execute(
            select(WebUser).filter_by(username=user.username)
        )
        existing_user = result.scalar_one_or_none()  # Вернет None, если пользователь не найден
        if existing_user:
            raise HTTPException(status_code=400, detail="Пользователь существует")

        # Хэшируем пароль
        hashed_password = pwd_context.hash(user.password)

        # Создаем нового пользователя
        new_user = WebUser(
            username=user.username,
            password=hashed_password,
            role=user.role,
            last_name="",
            first_name="",
            full_name=user.username,  # Заполняем как минимум полное имя
            email=f"{user.username}@example.com",  # Заполнение примерным email
            login=user.username  # Добавлено поле login
        )
        session.add(new_user)
        await session.commit()

        # Создаем токены с ролью пользователя в payload
        access_token = create_tokens(data={"sub": user.username, "role": user.role})
        refresh_token = create_tokens(data={"sub": user.username, "role": user.role}, expires_delta=timedelta(days=7))

        await save_token(new_user.id, refresh_token)

        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, max_age=604800)

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
async def login_user(user: UserLogin, response: Response):
    # Создаем сессию базы данных вручную
    async with async_session() as session:
        # Ищем пользователя в базе данных
        result = await session.execute(
            select(WebUser).filter_by(username=user.username)
        )
        existing_user = result.scalar_one_or_none()  # Вернет None, если пользователь не найден
        if not existing_user:
            raise HTTPException(status_code=401, detail="Пользователь не найден")

        # Проверяем, совпадает ли введенный пароль с хэшированным
        if not pwd_context.verify(user.password, existing_user.password):
            raise HTTPException(status_code=401, detail="Неверный логин или пароль")

        # Создаем токены с ролью пользователя в payload
        access_token = create_tokens(data={"sub": user.username, "role": existing_user.role})
        refresh_token = create_tokens(data={"sub": user.username, "role": existing_user.role}, expires_delta=timedelta(days=7))
        await save_token(existing_user.id, refresh_token)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, max_age=604800)

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
async def refresh_token(request: Request, response: Response):
    async with async_session() as session:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=403, detail="Refresh token невалидный")
        # Декодируем refresh token из cookies
        user_data = validate_refresh_token(refresh_token)
        # Ищем токен в бд
        token_query = await session.execute(
            select(TokenSchema).filter_by(refresh_token=refresh_token)
        )
        token_data = token_query.scalar_one_or_none()
        if not user_data or not token_data:
            raise HTTPException(status_code=403, detail="Refresh token невалидный")

        user_id = token_data.user_id

        user_query = await session.execute(
            select(WebUser).filter_by(id=user_id)
        )
        user = user_query.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        access_token = create_tokens(data={"sub": user.username, "role": user.role})
        refresh_token = create_tokens(data={"sub": user.username, "role": user.role},
                                      expires_delta=timedelta(days=7))
        await save_token(user.id, refresh_token)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, max_age=604800)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "username": user.username,
                "role": user.role,
                "id": user.id,
            },
        }


@router.get("/logout")
async def logout_user(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")

    if refresh_token:
        await remove_token(refresh_token)

    # Delete the refresh_token cookie
    response.delete_cookie(key="refresh_token")

    # Return the refresh_token in the JSON response
    return {"refresh_token": refresh_token}


@router.get("/tokens", response_model=None)
async def get_all_tokens():
    async with async_session() as session:
        # Query to get all tokens
        result = await session.execute(select(TokenSchema))
        tokens = result.scalars().all()  # Get all token records

    return tokens
