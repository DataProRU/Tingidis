from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request, Form, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
from sqlalchemy import update
from web_app.database import async_session, WebUser
from web_app.database import get_db
from web_app.services.auth_service import  register_user
from fastapi.responses import HTMLResponse, RedirectResponse
import logging
from fastapi.templating import Jinja2Templates

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Конфигурация
SECRET_KEY = "your_secret_key"
REFRESH_SECRET_KEY = "your_refresh_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 3

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Модели
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    roles: list[str] | None = None

# Утилиты
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


router = APIRouter()
templates = Jinja2Templates(directory="web_app/templates")

@router.post("/register")
async def post_register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form(),
    db: AsyncSession = Depends(get_db),
):
    logger.info(f"Registering new user: {username}")
    try:
        await register_user(request, username, password, role, db, templates)
    except Exception as e:
        logger.error(f"Registration failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    logger.info(f"User {username} registered successfully")
    return RedirectResponse(url="/users", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(async_session)):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # Генерация токенов
    access_token = create_token(
        data={"sub": user.login, "roles": [user.role]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        secret_key=SECRET_KEY,
    )
    refresh_token = create_token(
        data={"sub": user.login},
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        secret_key=REFRESH_SECRET_KEY,
    )

    # Обновление refresh-токена в базе
    await session.execute(
        update(WebUser).where(WebUser.id == user.id).values(refresh_token=refresh_token)
    )
    await session.commit()

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(async_session)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login: str = payload.get("sub")
        roles: list[str] = payload.get("roles", [])
        if not login:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_login(session, login)
    if not user:
        raise credentials_exception

    return {
        "username": user.login,
        "roles": roles,
        "email": user.email,
        "full_name": user.full_name,
    }

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(async_session)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login: str = payload.get("sub")
        if not login:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_login(session, login)
    if not user:
        raise credentials_exception

    # Очистка refresh-токена в базе
    await session.execute(
        update(WebUser).where(WebUser.id == user.id).values(refresh_token=None)
    )
    await session.commit()

    return {"message": "Successfully logged out"}
