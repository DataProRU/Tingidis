from web_app.database import Base
from sqlalchemy import Column, Integer, String, Date, Text, Boolean
from sqlalchemy.orm import relationship


class Users(Base):
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
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    role = Column(String, server_default="user")
    notification = Column(Boolean, default=False)

    tokens = relationship("Tokens", back_populates="user", cascade="all, delete-orphan")
    contracts = relationship("Contracts", back_populates="executor_info")
    project_executors = relationship("ProjectExecutors", back_populates="user_info")
    projects = relationship("Projects", back_populates="executor_info")
