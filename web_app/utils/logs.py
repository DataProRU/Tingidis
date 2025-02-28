from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from bot import notify_user
from web_app.models import LogEntry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_action(action: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_data = kwargs.get("user_data", {"sub": "Unknown"})
            username = user_data.get("sub", "Unknown")
            delete_id = kwargs.get("object_id", None)

            result = await func(*args, **kwargs)

            if isinstance(result, dict):
                object_id = result.get("id", delete_id)
            elif hasattr(result, "id"):
                object_id = getattr(result, "id", delete_id)
            else:
                object_id = delete_id

            logger.info(f"User '{username}' performed '{action}' on object (ID: {object_id})")
            session: AsyncSession = kwargs.get("db")
            log_entry = LogEntry(user=username, action=f"{action} (ID: {object_id})")
            session.add(log_entry)
            await session.commit()

            logger.info(f"Sending notification to user '{username}'")
            try:
                # Отправляем уведомление
                await notify_user(username, f"Произошло действие: {action} (ID: {object_id})")
            except Exception as e:
                logger.error(f"Error sending notification for user '{username}': {e}")

            return result

        return wrapper

    return decorator
