from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request, Form, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from sqlalchemy import update
from web_app.database import async_session, WebUser
from web_app.database import get_db
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
import logging
from fastapi.templating import Jinja2Templates
from sqlalchemy.future import select
from typing import Dict
from web_app.schemas.token import Token, TokenData
from web_app.services.auth_service import (
    authenticate_user,
    create_token,
    get_user_by_login,
    SECRET_KEY,
    REFRESH_SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    oauth2_scheme,
)
from pydantic import BaseModel, Field
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="web_app/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, example="john_doe")
    password: str = Field(..., min_length=6, example="securepassword123")
    role: Optional[str] = Field(default="user", example="admin")

# Function to hash passwords
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Registration endpoint
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user_endpoint(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        # Check if the username already exists
        existing_user = await get_user_by_login(db, request.username)
        if existing_user:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "User with this username already exists"}
            )

        # Create a new user
        new_user = WebUser(
            username=request.username,
            password=get_password_hash(request.password),  # Hash the password
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
            role=request.role,
            login=request.username,  # Use the provided username as login
        )

        # Add the user to the database
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "User registered successfully", "user_id": new_user.id}
        )

    except Exception as e:
        # General error handling
        await db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "An unexpected error occurred", "details": str(e)}
        )

class LoginRequest(BaseModel):
    username: str
    password: str

# Модель запроса для логина
class LoginRequest(BaseModel):
    username: str
    password: str

# Модель пользователя
class User(BaseModel):
    id: int
    username: str
    password: str
    role: str

# Функция для хеширования паролей
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Функция для проверки пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Функция для создания токена
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Функция для аутентификации пользователя
async def authenticate_user(session: AsyncSession, username: str, password: str) -> Optional[User]:
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user or not verify_password(password, user.password):
        return None
    return user

# Эндпоинт для логина
@router.post("/auth/login", response_model=dict)
async def login(request: LoginRequest, session: AsyncSession = Depends(async_session)):
    user = await authenticate_user(session, request.username, request.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")

    # Generate tokens
    access_token = create_access_token(
        data={"sub": user.username, "roles": [user.role]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )

    # Update refresh token in the database
    await session.execute(
        update(User).where(User.id == user.id).values(refresh_token=refresh_token)
    )
    await session.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/users/me")
async def read_users_me(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(async_session)
):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )
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
async def logout(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(async_session)
):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )
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

    # Clear refresh token in the database
    await session.execute(
        update(WebUser).where(WebUser.id == user.id).values(refresh_token=None)
    )
    await session.commit()

    return {"message": "Successfully logged out"}
