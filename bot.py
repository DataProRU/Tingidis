from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from web_app.models import Users, LogEntry
import asyncio

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
async def command_start_handler(message: Message) -> None:
    await message.answer("Привет! Я бот для уведомлений.")

# Функция отправки уведомления
async def send_notification(telegram_username: str, message: str):
    try:
        await bot.send_message(chat_id=telegram_username, text=message)
    except Exception as e:
        print(f"Failed to send message to {telegram_username}: {e}")

# Функция уведомления пользователя
async def notify_user(session: AsyncSession, username: str, message: str):
    user = await session.execute(select(Users).where(Users.username == username))
    user = user.scalar_one_or_none()
    if user and user.notification and user.telegram:
        await send_notification(user.telegram, message)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())