from web_app.database import Base
from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    DECIMAL as Decimal,
)


class ContractsModel(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(Integer, ForeignKey("objects.id"), nullable=False)
    name = Column(String(50), nullable=False)

    number = Column(String(256), nullable=False, unique=True)
    sign_date = Column(DateTime, nullable=False, default=func.now())
    price = Column(Decimal, nullable=False)
    theme = Column(String(50), nullable=False)
    evolution = Column(String(30), nullable=False, default="Создан")
