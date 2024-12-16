from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from web_app.services.auth_service import login_user, register_user
from web_app.dependencies import (
    get_authenticated_user,
    get_current_user,
    get_token_from_cookie,
)
from web_app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import os

router = APIRouter()
templates = Jinja2Templates(directory="web_app/templates")
UPLOAD_DIRECTORY = "web_app/static/uploads"
LOGO_DIRECTORY = "web_app/static/img"


@router.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse(request, "register.html", {"request": request})


@router.post("/register")
async def post_register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form(),
    db: AsyncSession = Depends(get_db),
):
    try:
        await register_user(request, username, password, role, db, templates)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return RedirectResponse(url="/users", status_code=303)


@router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    logo_files = [f.name for f in os.scandir(LOGO_DIRECTORY) if f.is_file()]
    bg_files = [f.name for f in os.scandir(UPLOAD_DIRECTORY) if f.is_file()]
    if logo_files and bg_files:
        logo_file = max(
            logo_files, key=lambda f: os.path.getctime(os.path.join(LOGO_DIRECTORY, f))
        )
        bg_file = max(
            bg_files, key=lambda f: os.path.getctime(os.path.join(UPLOAD_DIRECTORY, f))
        )
    else:
        logo_file = None
        bg_file = None
    return templates.TemplateResponse(
        request,
        "login.html",
        {
            "request": request,
            "error": None,
            "bg_filename": bg_file,
            "logo_file": logo_file,
        },
    )


@router.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await login_user(request, form_data, db, templates)
    except Exception as e:
        # Handle specific exceptions if possible
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/welcome", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
async def welcome(request: Request):
    token = get_token_from_cookie(request)
    if isinstance(token, RedirectResponse):
        return token

    payload = get_current_user(token)
    if isinstance(payload, RedirectResponse):
        return payload

    # Extract user information
    username = payload.get("sub")
    role = payload.get("role")

    logo_files = [f.name for f in os.scandir(LOGO_DIRECTORY) if f.is_file()]
    bg_files = [f.name for f in os.scandir(UPLOAD_DIRECTORY) if f.is_file()]
    if logo_files and bg_files:
        logo_file = max(
            logo_files, key=lambda f: os.path.getctime(os.path.join(LOGO_DIRECTORY, f))
        )
        bg_file = max(
            bg_files, key=lambda f: os.path.getctime(os.path.join(UPLOAD_DIRECTORY, f))
        )
    else:
        logo_file = None
        bg_file = None
    return templates.TemplateResponse(
        request,
        "welcome.html",
        {
            "request": request,
            "username": username,
            "role": role,
            "bg_filename": bg_file,
            "logo_file": logo_file,
        },
    )


@router.get("/confirm", response_class=HTMLResponse)
async def confirm(
    request: Request,
    user: dict = Depends(get_authenticated_user),
):
    if isinstance(user, RedirectResponse):
        return user  # If the user is not authenticated

    return templates.TemplateResponse(request, "confirm.html", {"request": request})


@router.get("/access", response_class=HTMLResponse)
async def access(request: Request):
    token = get_token_from_cookie(request)
    if isinstance(token, RedirectResponse):
        return token
    payload = get_current_user(token)
    if isinstance(payload, RedirectResponse):
        return payload
    username = payload.get("sub")
    role = payload.get("role")
    return templates.TemplateResponse(
        request,
        "access.html",
        {
            "request": request,
            "username": username,
            "role": role,
        },
    )
