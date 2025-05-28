from web_app.database import Base
from sqlalchemy import Column, Integer, String, Date, Text, Boolean
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "web_user"

    id = Column(Integer, primary_key=True, autoincrement=True)

    first_name = Column(String(256), nullable=True)
    last_name = Column(String(256), nullable=True)
    father_name = Column(String(256), nullable=True)
    full_name = Column(String(256), nullable=True)
    position = Column(String(256), nullable=True)
    phone = Column(String(256), unique=True, nullable=True)
    email = Column(String(256), unique=True, index=True, nullable=True)
    telegram = Column(String(256), unique=True, nullable=True)
    birthday = Column(Date, nullable=True)
    category = Column(String(256), nullable=True)
    specialization = Column(String(256), nullable=True)
    username = Column(String(256), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    notes = Column(Text, nullable=True)
    role = Column(String(256), server_default="user")
    notification = Column(Boolean, default=False)
    tg_user_id = Column(Integer, nullable=True)

    tokens = relationship("Tokens", back_populates="user", cascade="all, delete-orphan")
    contracts = relationship(
        "Contracts",
        back_populates="executor_info",
        cascade="all, delete-orphan",
        passive_deletes=False,
    )
    project_executors = relationship(
        "ProjectExecutors",
        back_populates="user_info",
        cascade="all, delete-orphan",
        passive_deletes=False,
    )
    projects = relationship(
        "Projects",
        back_populates="executor_info",
        cascade="all, delete-orphan",
        passive_deletes=False,
    )
    personal_settings = relationship(
        "PersonalSettings",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=False,
    )
