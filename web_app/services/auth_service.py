import logging
from fastapi import Request, status
from fastapi.responses import RedirectResponse

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from web_app.database import WebUser  # Assuming you have a User model
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


# Конфигурация
SECRET_KEY = "your_secret_key"
REFRESH_SECRET_KEY = "your_refresh_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 3

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_user_by_login(session: AsyncSession, login: str):
    query = select(WebUser).where(WebUser.login == login)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(session: AsyncSession, login: str, password: str):
    user = await get_user_by_login(session, login)
    if not user or not await verify_password(password, user.password):
        return None
    return user


def create_token(data: dict, expires_delta: timedelta, secret_key: str):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)


async def register_user(request, username, password, role, db, templates):
    try:
        logger.info(f"Registering user: {username}, role: {role}")
        new_user = WebUser(
            username=username,
            password=get_password_hash(password),
            last_name="Default Last Name",
            first_name="Default First Name",
            middle_name="Default Middle Name",
            full_name="Default Full Name",
            position="Default Position",
            phone="12345677",
            email="default@example.com",
            telegram="default_telegram",
            birthdate=datetime.strptime("2001-06-26", "%Y-%m-%d").date(),
            category="Default Category",
            specialization="Default Specialization",
            notes="Default Notes",
            role=role,
            login="Pavel",
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        logger.info(f"User {username} registered successfully")
        return RedirectResponse("/users", status_code=303)
    except Exception as e:
        logger.error(f"Error during user registration: {e}")
        return templates.TemplateResponse(
            "register.html", {"request": request, "error": str(e)}
        )

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Исправленная функция регистрации
async def register_user(request, username, password, role, db: AsyncSession):
    try:
        logger.info(f"Registering user: {username}, role: {role}")

        # Проверяем, существует ли пользователь с таким логином
        existing_user = await get_user_by_login(db, username)
        if existing_user:
            logger.warning(f"User with username {username} already exists")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "User with this username already exists"}
            )

        # Создаём нового пользователя
        new_user = WebUser(
            username=username,
            password=get_password_hash(password),  # Хэшируем пароль
            last_name="Default Last Name",
            first_name="Default First Name",
            middle_name="Default Middle Name",
            full_name="Default Full Name",
            position="Default Position",
            phone="12345677",
            email="default@example.com",
            telegram="default_telegram",
            birthdate=datetime.strptime("2001-06-26", "%Y-%m-%d").date(),
            category="Default Category",
            specialization="Default Specialization",
            notes="Default Notes",
            role=role,
            login=username,  # Используем переданный username как login
        )

        # Добавляем пользователя в базу данных
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        logger.info(f"User {username} registered successfully")
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "User registered successfully", "user_id": new_user.id}
        )

    except IntegrityError as e:
        # Обработка ошибок базы данных, например, уникальных ограничений
        logger.error(f"Database error during user registration: {e}")
        await db.rollback()
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Database error: user might already exist"}
        )
    except Exception as e:
        # Общая обработка ошибок
        logger.error(f"Error during user registration: {e}")
        await db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "An unexpected error occurred", "details": str(e)}
        )

