import logging
from fastapi import APIRouter, Request, Form, Depends, status, Header, HTTPException

from web_app.schemas.users import WebUser, WebUserResponse, WebUserCreate

from web_app.database import get_db
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from typing import List
from web_app.services.auth_middleware import token_verification_dependency

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="web_app/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/users/", response_model=List[WebUserResponse])
async def get_users(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    stmt = select(WebUser)
    result = await db.execute(stmt)
    users = result.scalars().all()
    return users


@router.get("/users/{user_id}", response_model=WebUserResponse)
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(select(WebUser).filter(WebUser.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@router.post(
    "/users", response_model=WebUserResponse, status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_data_create: WebUserCreate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    user = WebUser(**user_data_create.dict())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.patch("/users/{users_id}", response_model=WebUserResponse)
async def update_user(
    user_id: int,
    web_user_data: WebUserCreate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(select(WebUser).filter(WebUser.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    for key, value in web_user_data.dict(exclude_unset=True).items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    # user_data: dict = Depends(token_verification_dependency),
):
    # Проверка наличия объекта
    result = await db.execute(select(WebUser).filter(WebUser.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Удаление объекта
    await db.delete(user)
    await db.commit()
    return {"message": "Пользователь успешно удален", "user_id": user_id}
