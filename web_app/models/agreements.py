from sqlalchemy.orm import relationship

from web_app.database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Text,
    ForeignKey,
    DECIMAL as Decimal,
)


class Agreements(Base):
    __tablename__ = "agreements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    number = Column(String)
    price = Column(Decimal)
    deadline = Column(Date)
    notes = Column(Text, nullable=True)
    contract = Column(Integer, ForeignKey("contracts.id"))

    contract_info = relationship("Contracts", back_populates="agreements")
