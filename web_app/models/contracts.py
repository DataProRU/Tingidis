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


class Contracts(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(Integer, ForeignKey("objects.id"))
    name = Column(String(50))

    number = Column(String(256), unique=True)
    sign_date = Column(DateTime, default=func.now())
    price = Column(Decimal)
    theme = Column(String(50))
    evolution = Column(String(30), default="Создан")
