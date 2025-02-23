from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from web_app.database import Base


class ProjectExecutors(Base):
    __tablename__ = "project_executors"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey("web_user.id"))
    project = Column(Integer, ForeignKey("projects.id"))

    user_info = relationship("Users", back_populates="project_executors")
    project_info = relationship("Projects", back_populates="project_executors")
