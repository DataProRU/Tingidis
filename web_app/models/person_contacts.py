from web_app.database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
)


class PersonContracts(Base):
    __tablename__ = "person_contracts"

    id = Column(Integer, primary_key=True, autoincrement=True)

    first_name = Column(String(50))
    last_name = Column(String(50))
    father_name = Column(String(50))

    email = Column(String(50))
    position = Column(String(50))

    customer = Column(Integer, ForeignKey("customers.id"))
