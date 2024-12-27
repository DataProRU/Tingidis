import logging
from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
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
from web_app.services.storage import get_bg, get_logo

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="web_app/templates")


@router.get("/register", response_class=JSONResponse)
async def get_register(request: Request):
    logger.info("Accessing registration page")
    return {"request": str(request.url)}


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


@router.get("/login", response_class=JSONResponse)
async def get_login(request: Request):
    logger.info("Accessing login page")
    logo_file = await get_logo()
    bg_file = await get_bg()

    return {
        "request": str(request.url),
        "error": None,
        "bg_filename": bg_file,
        "logo_file": logo_file,
    }


@router.post("/login", response_class=JSONResponse)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    logger.info(f"Logging in user: {form_data.username}")
    try:
        return await login_user(request, form_data, db, templates)
    except Exception as e:
        logger.error(f"Login failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/welcome", response_class=JSONResponse)
@router.get("/", response_class=JSONResponse)
async def welcome(request: Request):
    logger.info("Accessing welcome page")
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

    # Extract user information
    username = payload.get("sub")
    role = payload.get("role")

    logo_file = await get_logo()
    bg_file = await get_bg()

    return {
        "request": str(request.url),
        "username": username,
        "role": role,
        "bg_filename": bg_file,
        "logo_file": logo_file,
    }


@router.get("/confirm", response_class=JSONResponse)
async def confirm(
    request: Request,
    user: dict = Depends(get_authenticated_user),
):
    logger.info("Accessing confirmation page")
    if isinstance(user, RedirectResponse):
        logger.warning("Unauthenticated user access attempt")
        return JSONResponse(
            content={"error": "Unauthenticated user access attempt"}, status_code=401
        )

    return {"request": str(request.url)}


@router.get("/access", response_class=JSONResponse)
async def access(request: Request):
    logger.info("Accessing access page")
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

    username = payload.get("sub")
    role = payload.get("role")

    return {
        "request": str(request.url),
        "username": username,
        "role": role,
    }
