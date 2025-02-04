from sqlalchemy.orm import relationship

from web_app.database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
)


class Contacts(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    father_name = Column(String(50))
    phone = Column(String(50))
    email = Column(String(50))
    position = Column(String(50))
    customer = Column(Integer, ForeignKey("customers.id"))

    customer_info = relationship("Customers", back_populates="contacts")
