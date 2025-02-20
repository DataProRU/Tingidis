from web_app.database import Base
from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date
)


class Backups(Base):
    __tablename__ = "backups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), nullable=False)
    frequency = Column(Integer, nullable=False)
    send_date = Column(Date, nullable=False)