from sqlalchemy import Column, Integer, String
from web_app.database import Base


class Customers(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String)
    inn = Column(String)
