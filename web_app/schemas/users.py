from pydantic import BaseModel, constr, EmailStr
from typing import Optional
from datetime import date


class UserResponse(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    father_name: Optional[str] = None
    full_name: Optional[str] = None
    position: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    telegram: Optional[str] = None
    birthday: Optional[date] = None
    category: Optional[str] = None
    specialization: Optional[str] = None
    username: str
    password: Optional[str] = None
    notes: Optional[str] = None
    role: str
    notification: Optional[bool] = None


class UserUpdate(BaseModel):
    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    father_name: Optional[str] = None
    full_name: Optional[str] = None
    position: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    telegram: Optional[str] = None
    birthday: Optional[date] = None
    category: Optional[str] = None
    specialization: Optional[str] = None
    username: str
    password: Optional[str] = None
    notes: Optional[str] = None
    role: str
    notification: Optional[bool] = None


class UserCreate(BaseModel):

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    father_name: Optional[str] = None
    full_name: Optional[str] = None
    position: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    telegram: Optional[str] = None
    birthday: Optional[date] = None
    category: Optional[str] = None
    specialization: Optional[str] = None
    username: str
    password: Optional[str] = None
    notes: Optional[str] = None
    role: str
    notification: Optional[bool] = False


# Модель запроса для регистрации
class UserRegister(BaseModel):
    username: str
    password: str
    role: str


# Модель запроса для входа
class UserLogin(BaseModel):
    username: str
    password: str
