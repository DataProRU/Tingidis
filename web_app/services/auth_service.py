import logging
from fastapi import Request, status
from fastapi.responses import RedirectResponse
from web_app.services.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
)
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from web_app.database import WebUser  # Assuming you have a User model
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

async def login_user(request: Request, form_data, db: AsyncSession, templates):
    try:
        logger.info(f"Logging in user: {form_data.username}")
        stmt = select(WebUser).where(WebUser.username == form_data.username)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        # Проверка, найден ли пользователь и совпадает ли пароль
        if user and verify_password(form_data.password, user.password):
            logger.info(f"User {form_data.username} authenticated successfully")
            # Генерация токена и установка куки
            token = create_access_token({"sub": form_data.username, "role": user.role})
            response = RedirectResponse(
                url="/welcome", status_code=status.HTTP_303_SEE_OTHER
            )
            response.set_cookie(key="token", value=token, httponly=True)
            return response

        # Ошибка авторизации
        logger.warning(f"Authentication failed for user: {form_data.username}")
        return templates.TemplateResponse(
            "login.html", {"request": request, "error": "Invalid username or password"}
        )

    except Exception as e:
        logger.error(f"Error logging in: {e}")
        return templates.TemplateResponse(
            "login.html", {"request": request, "error": "An error occurred"}
        )
