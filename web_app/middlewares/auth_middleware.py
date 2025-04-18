from fastapi import Depends, Request, HTTPException

from web_app.routes.auth import SECRET_KEY, ALGORITHM
from web_app.services.auth import validate_access_token


async def token_verification_dependency(request: Request):
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

    # Возвращаем данные пользователя для маршрута, если понадобится
    return user_data
