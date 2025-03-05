from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from web_app.database import get_db
from fastapi import Depends
from web_app.models.users import Users
from dotenv import load_dotenv
from passlib.context import CryptContext
import os

load_dotenv()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def add_first_user(db: AsyncSession = Depends(get_db)):

    password = os.getenv("FIRST_USER_PASSWORD")
    hashed_password = pwd_context.hash(password)
    first_user_data = {
        "username": "admin",
        "first_name": "Admin",
        "last_name": "Adminov",
        "full_name": "Adminov Admin",
        "role": "admin",
        "password": hashed_password,
    }

    # Выполните запрос для проверки существования пользователя
    stmt = select(Users).where(Users.username == first_user_data["username"])
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    # Если пользователь не существует, добавьте его
    if not existing_user:
        new_user = Users(
            username=first_user_data["username"],
            first_name=first_user_data["first_name"],
            last_name=first_user_data["last_name"],
            role=first_user_data["role"],
            password=first_user_data["password"],
        )
        db.add(new_user)
        await db.commit()
