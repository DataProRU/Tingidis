from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
from web_app.models.logs import LogEntry

def log_action(action: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Получаем пользователя из контекста или аргументов
            user = kwargs.get('user', 'Unknown')
            # Получаем ID объекта из аргументов
            object_id = kwargs.get('object_id', None)
            # Выполняем основную функцию
            result = await func(*args, **kwargs)
            # Логируем действие
            session: AsyncSession = kwargs.get('db')
            log_entry = LogEntry(user=user, action=f"{action} (ID: {object_id})")
            session.add(log_entry)
            await session.commit()
            return result
        return wrapper
    return decorator