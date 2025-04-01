from datetime import datetime

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import expression

from web_app.database import Base
from sqlalchemy import Column, Integer, String, Date, Text, Boolean, ForeignKey, Index, DateTime, text
from sqlalchemy.orm import relationship


class PersonalSettings(Base):
    __tablename__ = "user_ui_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("web_user.id"), nullable=False)
    component = Column(String(100), nullable=False)
    settings = Column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    user = relationship("Users", back_populates='personal_settings')

    __table_args__ = (
        Index("ix_user_component", "user_id", "component", unique=True),
    )