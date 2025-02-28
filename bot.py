from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from web_app.database import async_session  # Импортируйте async_session или создайте его вручную
from web_app.models import Users
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Замените на ваш токен бота
API_TOKEN = '6025298232:AAGoesIM_VvWi5pjHXPEZC_-11CLpjZN9xA'

# Инициализация бота и диспетчера
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)  # Указываем parse_mode здесь
)
dp = Dispatcher()


# Команда /start
@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f"Привет! Я бот для уведомлений.")
    # logger.info(message)
    user_id = message.from_user.id
    username = message.from_user.username
    logger.info("Подключение к базе и отправка тестового уведомления")
    # Создаем сессию вручную
    async with async_session() as session:
        user = await session.execute(select(Users).where(Users.telegram == username))
        user = user.scalar_one_or_none()
        if user:
            user.tg_user_id = user_id
            await session.commit()
            await session.refresh(user)
            await notify_user(session, username, "Telegram id успешно привязан.")
        else:
            logger.info(f"Пользователь с ником {username} не существует.")


# Функция отправки уведомления
async def send_notification(user_id: int, message: str):
    try:
        logger.info(f"Attempting to send message to {user_id}: {message}")
        await bot.send_message(chat_id=user_id, text=message)
        logger.info(f"Message sent successfully to {user_id}")
    except Exception as e:
        logger.exception(f"Failed to send message to {user_id}: {e}")


# Функция уведомления пользователя
async def notify_user(session: AsyncSession, username: str, message: str):
    user = await session.execute(select(Users).where(Users.telegram == username))
    user = user.scalar_one_or_none()
    if user and user.notification and user.tg_user_id:
        logger.info(f"User {username} found, notification enabled, telegram: {user.tg_user_id}")
        await send_notification(user.tg_user_id, message)
    else:
        logger.info(f"User {username} not found or notification disabled or you should start bot")


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())