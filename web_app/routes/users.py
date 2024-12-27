import logging
from fastapi import APIRouter, Request, Form, Depends, status
from web_app.database import WebUser, get_db
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from web_app.services.storage import get_logo, get_bg
from web_app.services.users_services import (
    get_all_users,
    add_new_user,
    delete_user_service,
    update_user_service,
)
from datetime import date
from web_app.dependencies import get_token_from_cookie, get_current_user

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/users/", response_class=JSONResponse)
async def get_users(request: Request, db: AsyncSession = Depends(get_db)):
    logger.info("Fetching users list")
    token = get_token_from_cookie(request)
    if isinstance(token, RedirectResponse):
        logger.warning("Unauthorized access attempt")
        return JSONResponse(
            content={"error": "Unauthorized access attempt"}, status_code=401
        )

    payload = get_current_user(token)
    if isinstance(payload, RedirectResponse):
        logger.warning("Invalid token")
        return JSONResponse(content={"error": "Invalid token"}, status_code=401)

    if payload.get("role") != "admin":
        logger.warning("Access denied for non-admin user")
        return JSONResponse(
            content={"error": "Access denied for non-admin user"}, status_code=403
        )

    users_data = await get_all_users(db)
    logo_file = await get_logo()
    bg_file = await get_bg()

    return {
        "request": str(request.url),
        "users": users_data,
        "bg_filename": bg_file,
        "logo_file": logo_file,
    }


@router.post("/users/{user_id}/edit/", response_class=JSONResponse)
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
    token = get_token_from_cookie(request)
    if isinstance(token, RedirectResponse):
        logger.warning("Unauthorized access attempt")
        return JSONResponse(
            content={"error": "Unauthorized access attempt"}, status_code=401
        )

    payload = get_current_user(token)
    if isinstance(payload, RedirectResponse):
        logger.warning("Invalid token")
        return JSONResponse(content={"error": "Invalid token"}, status_code=401)

    if payload.get("role") != "admin":
        logger.warning("Access denied for non-admin user")
        return JSONResponse(
            content={"error": "Access denied for non-admin user"}, status_code=403
        )

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
        return JSONResponse(
            content={"message": "User updated successfully"},
            status_code=status.HTTP_200_OK,
        )

    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error: {e}")
        return JSONResponse(
            {"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.post("/users/add/", response_class=JSONResponse)
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
    token = get_token_from_cookie(request)
    if isinstance(token, RedirectResponse):
        logger.warning("Unauthorized access attempt")
        return JSONResponse(
            content={"error": "Unauthorized access attempt"}, status_code=401
        )

    payload = get_current_user(token)
    if isinstance(payload, RedirectResponse):
        logger.warning("Invalid token")
        return JSONResponse(content={"error": "Invalid token"}, status_code=401)

    if payload.get("role") != "admin":
        logger.warning("Access denied for non-admin user")
        return JSONResponse(
            content={"error": "Access denied for non-admin user"}, status_code=403
        )

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
        return JSONResponse(
            content={"message": "User added successfully"},
            status_code=status.HTTP_201_CREATED,
        )

    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error: {e}")
        return JSONResponse(
            {"detail": "Database error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/users/{user_id}/", response_class=JSONResponse)
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

    return {
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


@router.post("/users/{user_id}/delete/", response_class=JSONResponse)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"Deleting user with user_id: {user_id}")
    try:
        await delete_user_service(user_id, db)
        return JSONResponse(
            content={"message": "User deleted successfully"},
            status_code=status.HTTP_200_OK,
        )
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error: {e}")
        return JSONResponse(
            {"detail": "Database error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
