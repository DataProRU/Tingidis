from web_app.database import Base
from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    DECIMAL as Decimal,
)


class BusinessContracts(Base):
    __tablename__ = "business_contracts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(Integer, ForeignKey("objects.id"), nullable=False)
    name = Column(String(50), nullable=False)
    customer = Column(Integer, ForeignKey("customers.id"), nullable=False)
    executor = Column(Integer, ForeignKey("web_user.id"), nullable=False)
    number = Column(String(256), unique=True, nullable=False)
    sign_date = Column(Date, default=func.now(), nullable=False)
    price = Column(Decimal, nullable=False)
    theme = Column(String(50), nullable=False)
    evolution = Column(String(30), nullable=False, default="Создан")
