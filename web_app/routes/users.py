import logging
from fastapi import APIRouter, Request, Form, Depends, status, Header, HTTPException
from web_app.database import WebUser, get_db
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext


from web_app.services.auth_middleware import token_verification_dependency
from web_app.services.users_services import (
    get_all_users,
    add_new_user,
    delete_user_service,
    update_user_service,
)
from datetime import date

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="web_app/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/users/", response_model=list[dict])
async def get_users_json(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    logger.info("Fetching users list in JSON format")
    print("work")
    print(user_data)

    # Получение данных из базы
    result = await db.execute(select(WebUser))
    users = result.scalars().all()

    # Преобразование объектов в словари
    users_data = [
        {
            "id": user.id,
            "username": user.username,
            "last_name": user.last_name,
            "first_name": user.first_name,
            "middle_name": user.middle_name,
            "full_name": user.full_name,
            "position": user.position,
            "phone": user.phone,
            "email": user.email,
            "telegram": user.telegram,
            "birthdate": str(user.birthdate) if user.birthdate else None,
            "category": user.category,
            "specialization": user.specialization,
            "notes": user.notes,
            "login": user.login,
            "role": user.role,
            # Пароль отображается только для администратора
            "password": user.password if user_data.get("role") == "admin" else None,
        }
        for user in users
    ]

    return JSONResponse(content=users_data)


@router.post("/users/{user_id}/edit/")
async def update_user(
    user_id: int,
    request: Request,
    role: str = Form(...),
    last_name: str = Form(...),
    first_name: str = Form(...),
    middle_name: str = Form(...),
    position: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    telegram: str = Form(...),
    birthdate: date = Form(...),
    category: str = Form(...),
    specialization: str = Form(...),
    notes: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    form_data = await request.form()
    logger.info(f"Form data received: {form_data}")

    try:

        await update_user_service(
            user_id,
            role,
            last_name,
            first_name,
            middle_name,
            position,
            phone,
            email,
            telegram,
            birthdate,
            category,
            specialization,
            notes,
            db,
        )
        logger.info(f"User {user_id} updated successfully")
        return RedirectResponse(url="/users/", status_code=status.HTTP_303_SEE_OTHER)

    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error: {e}")
        return JSONResponse(
            {"detail": str(e)}, status_code=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED
        )


@router.post("/users/add/")
async def add_user(
    request: Request,
    last_name: str = Form(...),
    first_name: str = Form(...),
    middle_name: str = Form(...),
    position: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    telegram: str = Form(...),
    birthdate: date = Form(...),
    category: str = Form(...),
    specialization: str = Form(...),
    notes: str = Form(...),
    login: str = Form(...),
    password: str = Form(...),
    role: str = Form("admin"),
    db: AsyncSession = Depends(get_db),
):

    try:
        await add_new_user(
            last_name,
            first_name,
            middle_name,
            position,
            phone,
            email,
            telegram,
            birthdate,
            category,
            specialization,
            notes,
            login,
            password,
            role,
            db,
        )
        logger.info(f"New user added: {login}")

        return RedirectResponse(url="/users/", status_code=status.HTTP_303_SEE_OTHER)

    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error: {e}")
        return JSONResponse(
            {"detail": "Database error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/users/{user_id}/")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"Fetching user details for user_id: {user_id}")
    stmt = select(WebUser).where(WebUser.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        logger.error(f"User not found: {user_id}")
        return JSONResponse(
            {"detail": "User not found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    return JSONResponse(
        {
            "id": user.id,
            "last_name": user.last_name,
            "first_name": user.first_name,
            "middle_name": user.middle_name,
            "position": user.position,
            "phone": user.phone,
            "email": user.email,
            "telegram": user.telegram,
            "birthdate": user.birthdate.isoformat(),
            "category": user.category,
            "specialization": user.specialization,
            "notes": user.notes,
            "login": user.login,
        }
    )


@router.post("/users/{user_id}/delete/")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"Deleting user with user_id: {user_id}")
    try:
        await delete_user_service(user_id, db)

        return RedirectResponse(url="/users/", status_code=status.HTTP_303_SEE_OTHER)
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error: {e}")
        return JSONResponse(
            {"detail": "Database error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
