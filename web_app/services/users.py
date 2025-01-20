from web_app.database import get_db
from web_app.schemas.users import Users
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends
from datetime import date
import logging
from passlib.context import CryptContext

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_all_users(db: AsyncSession = Depends(get_db)) -> list:
    stmt = select(Users)
    result = await db.execute(stmt)
    users = result.scalars().all()

    return users


async def get_user_by_id(user_id: int, db: AsyncSession) -> Users | None:
    stmt = select(Users).where(Users.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        logger.error(f"User not found: {user_id}")
        return None
    return user


async def update_user_service(
    user_id: int,
    role: str,
    last_name: str,
    first_name: str,
    middle_name: str,
    position: str,
    phone: str,
    email: str,
    telegram: str,
    birthdate: date,
    category: str,
    specialization: str,
    notes: str,
    db,
) -> None:
    user = await get_user_by_id(user_id, db)
    if not user:
        logger.error(f"User not found {user_id}")
        return None

    initials = (
        f"{first_name[0].upper()}. {middle_name[0].upper()}."
        if middle_name
        else f"{first_name[0].upper()}."
    )

    user.role = role
    user.last_name = last_name
    user.first_name = first_name
    user.middle_name = middle_name
    user.full_name = f"{last_name} {initials}"
    user.position = position
    user.phone = phone
    user.email = email
    user.telegram = telegram
    user.birthdate = birthdate
    user.category = category
    user.specialization = specialization
    user.notes = notes

    await db.commit()
    await db.refresh(user)
    logger.info(f"User with ID {user_id} updated successfully by service")

    return None


async def add_new_user(
    last_name: str,
    first_name: str,
    middle_name: str,
    position: str,
    phone: str,
    email: str,
    telegram: str,
    birthdate: date,
    category: str,
    specialization: str,
    notes: str,
    login: str,
    password: str,
    role: str,
    db,
) -> None:
    hashed_password = pwd_context.hash(password)
    initials = (
        f"{first_name[0].upper()}. {middle_name[0].upper()}."
        if middle_name
        else f"{first_name[0].upper()}."
    )
    new_user = Users(
        username=login,
        last_name=last_name,
        first_name=first_name,
        full_name=f"{last_name} {initials}",
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
    logger.info(f"New user added: {new_user.username} by service")

    return None


async def delete_user_service(user_id: int, db) -> None:
    user = await get_user_by_id(user_id, db)
    if not user:
        logger.error(f"User not found {user_id}")
        return None

    await db.delete(user)
    await db.commit()
    logger.info(f"User {user_id} deleted successfully")
