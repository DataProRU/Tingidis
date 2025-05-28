from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from web_app.database import Base


class FormOfOwnerships(Base):
    __tablename__ = "form_of_ownership"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))

    customers = relationship(
        "Customers",
        back_populates="form_of_ownership",
        cascade="all, delete-orphan",  # SQLAlchemy удалит связанные записи
        passive_deletes=False,
    )
