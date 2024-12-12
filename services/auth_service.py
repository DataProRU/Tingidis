from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from services.auth import verify_password, get_password_hash, create_access_token
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import WebUser  # Assuming you have a User model
from datetime import datetime


async def register_user(request, username, password, role, db, templates):
    try:
        print(f"Registering user: {username}, role: {role}")
        new_user = WebUser(
            username=username,
            password=get_password_hash(password),
            last_name="Default Last Name",
            first_name="Default First Name",
            middle_name="Default Middle Name",
            full_name="Default Full Name",
            position="Default Position",
            phone=1234567890,
            email="default@example.com",
            telegram="default_telegram",
            birthdate=datetime.strptime("2001-06-26", "%Y-%m-%d").date(),
            category="Default Category",
            specialization="Default Specialization",
            notes="Default Notes",
            role=role,
            login="Pavel",
        )
        print(f"New user object: {new_user}")
        db.add(new_user)
        await db.commit()
        print("Transaction committed successfully.")
        await db.refresh(new_user)
        print(f"User registered with ID: {new_user.id}")
        return RedirectResponse("/users", status_code=303)
    except Exception as e:
        print(f"Error during user registration: {e}")
        return templates.TemplateResponse(
            "register.html", {"request": request, "error": str(e)}
        )


async def login_user(request: Request, form_data, db: AsyncSession, templates):
    try:
        # Use SQLAlchemy's select statement
        stmt = select(WebUser).where(WebUser.username == form_data.username)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        stmt = select(WebUser)
        result = await db.execute(stmt)
        users_data = result.scalars().all()
        print(f"All users  {users_data}")
        print(f"Form data username: {form_data.username}")
        print(f"User found: {user}")

        # Проверка, найден ли пользователь и совпадает ли пароль
        if user and verify_password(form_data.password, user.password):
            # Генерация токена и установка куки
            token = create_access_token({"sub": form_data.username, "role": user.role})
            response = RedirectResponse(
                url="/welcome", status_code=status.HTTP_303_SEE_OTHER
            )
            response.set_cookie(key="token", value=token, httponly=True)
            return response

        # Ошибка авторизации
        return templates.TemplateResponse(
            "login.html", {"request": request, "error": "Invalid username or password"}
        )

    except Exception as e:
        # Логирование ошибки для отладки (по желанию)
        print(f"Error logging in: {e}")
        return templates.TemplateResponse(
            "login.html", {"request": request, "error": "An error occurred"}
        )
