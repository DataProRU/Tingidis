from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(..., title="Имя пользователя", example="testuser")
    password: str = Field(..., title="Пароль", example="password123")
    role: str = Field(..., title="Роль пользователя", example="user")


# Модель запроса для входа
class UserLogin(BaseModel):
    username: str
    password: str
