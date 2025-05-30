from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from web_app.database import Base


class ProjectStatuses(Base):
    __tablename__ = "project_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))

    projects = relationship(
        "Projects",
        back_populates="project_info",
        cascade="all, delete-orphan",
        passive_deletes=False,
    )
