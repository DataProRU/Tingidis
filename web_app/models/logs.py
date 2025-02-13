from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from web_app.database import Base


class LogEntry(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime, default=datetime.now)
    user = Column(String)
    action = Column(String)
