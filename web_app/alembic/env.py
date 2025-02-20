from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from alembic import context
from database import Base  # Убедитесь, что путь правильный
import os

# Настройка логирования
config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

# Подключаем метаданные моделей
target_metadata = Base.metadata


# Функция для получения URL базы данных
def get_url():
    return os.getenv(
        "DATABASE_URL", "postgresql+asyncpg://admin:2606QWmg@localhost:5432/users"
    )


# Создание асинхронного движка
async_engine = create_async_engine(get_url(), poolclass=pool.NullPool)


# Функция для выполнения миграций в асинхронном режиме
async def run_migrations():
    async with async_engine.connect() as connection:
        await connection.run_sync(do_run_migrations)


# Запуск миграций
def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    context.run_migrations()
