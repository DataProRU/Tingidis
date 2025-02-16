from web_app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    DECIMAL as Decimal,
)


class Contracts(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(Integer, ForeignKey("objects.id"))
    name = Column(String(50))
    customer = Column(Integer, ForeignKey("customers.id"))
    executor = Column(Integer, ForeignKey("web_user.id"))
    number = Column(String(256), unique=True)
    sign_date = Column(Date, default=func.now())
    price = Column(Decimal)
    theme = Column(String(50))
    evolution = Column(String(30))

    code_info = relationship("Objects", back_populates="contracts")
    customer_info = relationship("Customers", back_populates="contracts")
    executor_info = relationship("Users", back_populates="contracts")
    agreements = relationship("Agreements", back_populates="contract_info")
    projects = relationship("Projects", back_populates="contract_info")

    @staticmethod
    def generate_evolution(session):
        """Формирует evolution как порядковый номер + текущая дата/время"""
        last_entry = session.query(Contracts).order_by(Contracts.id.desc()).first()
        next_number = (
            (int(last_entry.evolution.split()[0]) + 1)
            if last_entry and last_entry.evolution
            else 1
        )
        timestamp = func.now()
        return f"{next_number} {timestamp}"

    def before_insert(self, session):
        """Проставляет evolution перед добавлением записи"""
        if not self.evolution:  # Только если не задано вручную
            self.evolution = self.generate_evolution(session)
