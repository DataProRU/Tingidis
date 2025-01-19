from pydantic import BaseModel
from datetime import date


class WebUserResponse(BaseModel):

    first_name: str
    last_name: str
    father_name: str
    full_name: str
    position: str
    phone: str
    email: str
    telegram: str
    birthday: date
    category: str
    specialization: str
    username: str
    password: str
    notes: str
    role: str


class WebUserCreate(BaseModel):

    first_name: str
    last_name: str
    father_name: str
    full_name: str
    position: str
    phone: str
    email: str
    telegram: str
    birthday: date
    category: str
    specialization: str
    username: str
    password: str
    notes: str
    role: str


# Модель запроса для регистрации
class UserCreate(BaseModel):
    username: str
    password: str
    role: str


# Модель запроса для входа
class UserLogin(BaseModel):
    username: str
    password: str
