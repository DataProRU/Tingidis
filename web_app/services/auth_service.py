from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from web_app.database import WebUser, TokenBlacklist
from fastapi import HTTPException, status
from sqlalchemy import select

# Настройка для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Секретный ключ и алгоритм для JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"


# Функция для создания токенов
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Общие функции
async def get_user_by_username(username: str, session: AsyncSession):
    result = await session.execute(select(WebUser).filter_by(username=username))
    return result.scalar_one_or_none()


async def add_token_to_blacklist(token: str, session: AsyncSession):
    session.add(TokenBlacklist(token=token))
    await session.commit()


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Срок действия токена истек",
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен"
        )
