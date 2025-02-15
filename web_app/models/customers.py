from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from web_app.database import Base


class Customers(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    form = Column(Integer, ForeignKey("form_of_ownership.id"))
    name = Column(String)
    address = Column(String)
    inn = Column(String)
    notes = Column(Text, nullable=True)

    form_of_ownership = relationship("FormOfOwnerships", back_populates="customers")
    contacts = relationship("Contacts", back_populates="customer_info")
    contracts = relationship("Contracts", back_populates="customer_info")
