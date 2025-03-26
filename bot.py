from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from web_app.database import (
    async_session,
)  # Импортируйте async_session или создайте его вручную
from web_app.models import Users
import asyncio
import logging
import os
from dotenv import load_dotenv


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

# Инициализация бота и диспетчера
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    ),  # Указываем parse_mode здесь
)
dp = Dispatcher()


# Команда /start
@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f"Привет! Я бот для уведомлений")
    # logger.info(message)
    tg_user_id = message.from_user.id
    tg_username = message.from_user.username
    logger.info("Attempting to connect to database and send test notification")
    # Создаем сессию вручную
    async with async_session() as session:
        user = await session.execute(select(Users).where(Users.telegram == tg_username))
        user = user.scalar_one_or_none()
        if user:
            user.tg_user_id = tg_user_id
            await session.commit()
            await session.refresh(user)
            await send_notification(tg_user_id, "Telegram id успешно привязан")
        else:
            logger.info(f"User with telegram username {tg_username} does not exist")


# Функция отправки уведомления
async def send_notification(user_id: int, message: str):
    try:
        logger.info(f"Attempting to send message to {user_id}: {message}")
        await bot.send_message(chat_id=user_id, text=message)
        logger.info(f"Message sent successfully to {user_id}")
    except Exception as e:
        logger.exception(f"Failed to send message to {user_id}: {e}")


# Функция массовых уведомлений пользователей
async def notify_all_users(session: AsyncSession, message: str):
    # Выбираем всех пользователей с включенными уведомлениями и указанным tg_user_id
    result = await session.execute(
        select(Users).where(
            Users.notification == True,
            Users.tg_user_id.is_not(None)
        )
    )
    users = result.scalars().all()

    logger.info(f"Starting notifications broadcast for {len(users)} users")

    # Отправляем уведомления каждому пользователю
    for user in users:
        try:
            await send_notification(user.tg_user_id, message)
            logger.info(f"Notification sent to {user.username} (ID: {user.tg_user_id})")
        except Exception as e:
            logger.error(f"Failed to send notification to {user.username}: {str(e)}")

    logger.info(f"Notifications broadcast completed. Total processed: {len(users)} users")

# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
