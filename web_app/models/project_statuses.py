from sqlalchemy import Column, Integer, String
from web_app.database import Base


class ProjectStatuses(Base):
    __tablename__ = "project_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30))