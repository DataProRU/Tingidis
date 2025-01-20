from sqlalchemy.testing.fixtures import TestBase
from web_app.database import Base
from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.orm import relationship


class Users(Base, TestBase):
    __tablename__ = "web_user"

    id = Column(Integer, primary_key=True, autoincrement=True)

    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    father_name = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    position = Column(String, nullable=True)
    phone = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    telegram = Column(String, unique=True, nullable=True)
    birthday = Column(Date, nullable=True)
    category = Column(String, nullable=True)
    specialization = Column(String, nullable=True)
    username = Column(
        String,
        unique=True,
    )
    password = Column(String)
    notes = Column(Text, nullable=True)
    role = Column(String, server_default="user")

    tokens = relationship("Tokens", back_populates="user", cascade="all, delete-orphan")
