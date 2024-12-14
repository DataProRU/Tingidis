from fastapi import APIRouter, Request, Form, Depends
from database import WebUser, get_db
from fastapi.templating import Jinja2Templates
from dependencies import get_token_from_cookie, get_current_user
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from passlib.context import CryptContext
from datetime import date
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")
UPLOAD_DIRECTORY = "static/uploads"
LOGO_DIRECTORY = "static/img"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/users/")
async def get_users(request: Request, db: AsyncSession = Depends(get_db)):
    token = get_token_from_cookie(request)
    if isinstance(token, RedirectResponse):
        return token

    payload = get_current_user(token)
    if isinstance(payload, RedirectResponse):
        return payload

    if payload.get("role") != "admin":
        return templates.TemplateResponse("not_access.html", {"request": request})

    stmt = select(WebUser)
    result = await db.execute(stmt)
    users_data = result.scalars().all()
    logo_files = os.listdir(LOGO_DIRECTORY)
    bg_files = os.listdir(UPLOAD_DIRECTORY)
    if logo_files and bg_files:
        logo_file = max(logo_files, key=lambda f: os.path.getctime(os.path.join(LOGO_DIRECTORY, f)))
        bg_file = max(bg_files, key=lambda f: os.path.getctime(os.path.join(UPLOAD_DIRECTORY, f)))
    else:
        logo_file = None
        bg_file = None
    return templates.TemplateResponse("users.html", {"request": request, "users": users_data, "bg_filename": bg_file, "logo_file":logo_file})


@router.post("/users/{user_id}/edit/")
async def update_user(
    user_id: int,
    request: Request,
    role: str = Form(...),
    last_name: str = Form(...),
    first_name: str = Form(...),
    middle_name: str = Form(...),
    position: str = Form(...),
    phone: int = Form(...),
    email: str = Form(...),
    telegram: str = Form(...),
    birthdate: date = Form(...),
    category: str = Form(...),
    specialization: str = Form(...),
    notes: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    form_data = await request.form()
    print("Данные формы:", form_data)
    token = get_token_from_cookie(request)
    if isinstance(token, RedirectResponse):
        return token

    payload = get_current_user(token)
    if isinstance(payload, RedirectResponse):
        return payload

    if payload.get("role") != "admin":
        return templates.TemplateResponse("not_access.html", {"request": request})

    try:
        stmt = select(WebUser).where(WebUser.id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return JSONResponse({"detail": "User not found"}, status_code=404)

        # Обновляем данные пользователя
        user.role = role
        user.last_name = last_name
        user.first_name = first_name
        user.middle_name = middle_name
        user.position = position
        user.phone = phone
        user.email = email
        user.telegram = telegram
        user.birthdate = birthdate
        user.category = category
        user.specialization = specialization
        user.notes = notes

        await db.commit()
        return RedirectResponse(url="/users/", status_code=303)

    except SQLAlchemyError as e:
        await db.rollback()
        return JSONResponse({"detail": str(e)}, status_code=500)

@router.post("/users/add/")
async def add_user(
    request: Request,
    username: str = Form("nono"),
    last_name: str = Form(...),
    first_name: str = Form(...),
    middle_name: str = Form(...),
    position: str = Form(...),
    phone: int = Form(...),
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
        return token

    payload = get_current_user(token)
    if isinstance(payload, RedirectResponse):
        return payload

    if payload.get("role") != "admin":
        return templates.TemplateResponse("not_access.html", {"request": request})

    try:
        hashed_password = pwd_context.hash(password)

        new_user = WebUser(
            username=username,
            last_name=last_name,
            first_name=first_name,
            full_name = last_name + first_name,
            middle_name=middle_name,
            position=position,
            phone=phone,
            email=email,
            telegram=telegram,
            birthdate=birthdate,
            category=category,
            specialization=specialization,
            notes=notes,
            login=login,
            password=hashed_password,
            role=role,
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return RedirectResponse(url="/users/", status_code=303)

    except SQLAlchemyError as e:
        await db.rollback()
        return JSONResponse({"detail": "Database error"}, status_code=500)

@router.get("/users/{user_id}/")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(WebUser).where(WebUser.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        return JSONResponse({"detail": "User not found"}, status_code=404)

    return JSONResponse({
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
    })

@router.post("/users/{user_id}/delete/")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(WebUser).where(WebUser.id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return templates.TemplateResponse("not_found.html", {"request": Request()})

        await db.delete(user)
        await db.commit()

        return RedirectResponse(url="/users/", status_code=303)
    except SQLAlchemyError as e:
        await db.rollback()
        return JSONResponse({"detail": "Database error"}, status_code=500)
