from fastapi import Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from web_app.routes.auth import SECRET_KEY, ALGORITHM
from web_app.services.auth import validate_access_token
from web_app.database import get_db
from web_app.models import Users, Tokens


async def token_verification_dependency(request: Request, db: AsyncSession = Depends(get_db)):
    authorization = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(status_code=401, detail="Отсутствует токен")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Неверный формат токена")

    # Извлекаем и валидируем токен
    user_token = authorization.split("Bearer ")[1]
    user_data = validate_access_token(
        access_token=user_token, key=SECRET_KEY, algoritm=ALGORITHM
    )
    if not user_data:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")

    # Проверяем, что текущий access_token соответствует активной сессии
    username = user_data["sub"]
    user_query = await db.execute(select(Users).filter_by(username=username))
    user = user_query.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    token_query = await db.execute(select(Tokens).filter_by(user_id=user.id))
    token_data = token_query.scalar_one_or_none()
    if not token_data or token_data.refresh_token != request.cookies.get("refresh_token"):
        raise HTTPException(status_code=401, detail="Сессия устарела")

    # Возвращаем данные пользователя для маршрута, если понадобится
    return user_data
