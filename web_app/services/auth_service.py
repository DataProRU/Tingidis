from datetime import datetime, timedelta
from sqlalchemy import select

import jwt

from web_app.database import async_session
from web_app.schemas.token import TokenSchema

# Функция для создания токенов
def create_token(
    data: dict, algoritm, key, expires_delta: timedelta = timedelta(minutes=15)
):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, key, algorithm=algoritm)


async def save_token(user_id, refresh_token):
    async with async_session() as session:
        async with session.begin():
            # Query for the existing token
            token_query = await session.execute(
                select(TokenSchema).filter_by(user_id=user_id)
            )
            existing_token = token_query.scalar_one_or_none()

            if existing_token:
                # Update the existing token's refresh_token
                existing_token.refresh_token = refresh_token
            else:
                # Create a new TokenSchema instance if no existing token is found
                new_token = TokenSchema(user_id=user_id, refresh_token=refresh_token)
                session.add(new_token)

        # Commit the transaction
        await session.commit()


async def remove_token(refresh_token):
    async with async_session() as session:
        async with session.begin():
            # Query for the token to be deleted
            token_query = await session.execute(
                select(TokenSchema).filter_by(refresh_token=refresh_token)
            )
            token_to_delete = token_query.scalar_one_or_none()

            if token_to_delete:
                # Delete the token if it exists
                await session.delete(token_to_delete)

        # Commit the transaction
        await session.commit()


def validate_access_token(access_token, key, algoritm):
    try:
        user_data = jwt.decode(access_token, key, algorithms=[algoritm])
        return user_data
    except Exception as e:
        return None


def validate_refresh_token(refresh_token, key, algoritm):
    try:
        user_data = jwt.decode(refresh_token, key, algorithms=[algoritm])
        return user_data
    except Exception as e:
        return None
