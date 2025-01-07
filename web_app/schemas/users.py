from pydantic import BaseModel

# Модель запроса для регистрации
class UserCreate(BaseModel):
    username: str
    password: str
    role: str

# Модель запроса для входа
class UserLogin(BaseModel):
    username: str
    password: str