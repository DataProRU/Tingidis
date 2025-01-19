from sqlalchemy.testing.fixtures import TestBase
from web_app.database import Base
from sqlalchemy import Column, Integer, String, Date, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


class WebUser(Base, TestBase):
    __tablename__ = "web_user"

    id = Column(Integer, primary_key=True, autoincrement=True)

    first_name = Column(String)
    last_name = Column(String)
    father_name = Column(String)
    full_name = Column(String)
    position = Column(String)
    phone = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    telegram = Column(
        String,
        unique=True,
    )
    birthday = Column(Date)
    category = Column(String)
    specialization = Column(String)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    notes = Column(Text)
    role = Column(String, nullable=False, server_default="user")

    tokens = relationship(
        "TokenSchema", back_populates="user", cascade="all, delete-orphan"
    )
