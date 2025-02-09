from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
from .models import LogEntry

def log_action(action: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Получаем пользователя из контекста или аргументов
            user = kwargs.get('user', 'Unknown')
            # Выполняем основную функцию
            result = await func(*args, **kwargs)
            # Логируем действие
            session: AsyncSession = kwargs.get('db')
            log_entry = LogEntry(user=user, action=action)
            session.add(log_entry)
            await session.commit()
            return result
        return wrapper
    return decorator