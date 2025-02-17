from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from web_app.database import Base


class ProjectExecutors(Base):
    __tablename__ = "project_executors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("web_user.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    user = relationship("Users", back_populates="project_executors")
    # project = relationship("Projects", back_populates="project_info")
