from web_app.database import Base
from sqlalchemy.testing.fixtures import TestBase
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Tokens(Base, TestBase):
    __tablename__ = "token_schema"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("web_user.id"), nullable=False)
    refresh_token = Column(String)

    user = relationship("Users", back_populates="tokens")
