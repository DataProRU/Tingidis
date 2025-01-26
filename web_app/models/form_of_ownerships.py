from sqlalchemy import Column, Integer, String
from web_app.database import Base


class FormOfOwnerships(Base):
    __tablename__ = "form_of_ownership"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), nullable=False)
