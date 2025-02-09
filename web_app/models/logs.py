from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class LogEntry(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime, default=datetime.now)
    user = Column(String, index=True)
    action = Column(String)