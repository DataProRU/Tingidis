from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from web_app.database import WebUser, async_session, TokenBlacklist
from sqlalchemy import select
from fastapi import Cookie, Depends, Response


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
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register")
async def register_user(user: UserCreate):
    # Создаем сессию базы данных вручную
    async with async_session() as session:
        # Проверяем, существует ли пользователь с таким логином
        result = await session.execute(
            select(WebUser).filter_by(username=user.username)
        )
        existing_user = result.scalar_one_or_none()  # Вернет None, если пользователь не найден
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

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
        access_token = create_access_token(data={"sub": user.username, "role": user.role})
        refresh_token = create_access_token(data={"sub": user.username, "role": user.role}, expires_delta=timedelta(days=7))

    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/login")
async def login_user(user: UserLogin):
    # Создаем сессию базы данных вручную
    async with async_session() as session:
        # Ищем пользователя в базе данных
        result = await session.execute(
            select(WebUser).filter_by(username=user.username)
        )
        existing_user = result.scalar_one_or_none()  # Вернет None, если пользователь не найден
        if not existing_user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Проверяем, совпадает ли введенный пароль с хэшированным
        if not pwd_context.verify(user.password, existing_user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Создаем токены с ролью пользователя в payload
        access_token = create_access_token(data={"sub": user.username, "role": existing_user.role})
        refresh_token = create_access_token(data={"sub": user.username, "role": existing_user.role}, expires_delta=timedelta(days=7))

    return {"access_token": access_token, "refresh_token": refresh_token}

@router.get("/refresh")
async def refresh_token(response: Response, refresh_token: str = Cookie(None)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token not provided")

    try:
        # Декодируем refresh token из cookies
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")

        if not username or not role:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Генерируем новый access token
        new_access_token = create_access_token(data={"sub": username, "role": role})

        # Устанавливаем новый access token в cookies, если нужно
        response.set_cookie(key="access_token", value=new_access_token, httponly=True)

        return {"access_token": new_access_token}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")