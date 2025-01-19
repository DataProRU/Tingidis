from web_app.database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Text,
    ForeignKey,
)


class AgreementsModel(Base):
    __tablename__ = "agreements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    number = Column(String, nullable=False)
    deadline = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    contract = Column(Integer, ForeignKey("contracts.id"), nullable=False)

    # tokens = relationship(
    #     "ContractsModel", back_populates="user", cascade="all, delete-orphan"
    # )
