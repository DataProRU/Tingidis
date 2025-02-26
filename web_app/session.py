from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

# Строка подключения к базе данных
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://admin:2606QWmg@localhost:5432/users"
)

async_engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем сессию
async def get_db():
    async with async_engine.begin() as conn:
        db = await sessionmaker(bind=conn)()
        yield db

# Закрываем сессию
async def close_db(db: AsyncSession):
    db.close()

# Создаем локальный класс сессии
class SessionLocal:
    def __enter__(self):
        return get_db()

    def __exit__(self, exc_type, exc_val, exc_tb):
        close_db(self)