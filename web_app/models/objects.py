from web_app.database import Base
from sqlalchemy import Column, Integer, String, Text


class ObjectModel(Base):
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(6), nullable=False)
    name = Column(String(30), nullable=False)
    comment = Column(Text, nullable=True)
