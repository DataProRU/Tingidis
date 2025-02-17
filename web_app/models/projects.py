import random
import string
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, event
from sqlalchemy.orm import relationship
from web_app.database import Base


def generate_project_number(object_id: int) -> str:
    letters = string.ascii_uppercase
    random_part = (
        f"{random.choice(letters)}{random.choice(letters)}-"
        f"{random.randint(0, 9)}-"
        f"{random.choice(letters.lower())}{random.choice(letters.lower())}{random.choice(letters.lower())}"
    )
    return f"{object_id}-{random_part}"


class Projects(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    object = Column(Integer, ForeignKey("objects.id"), nullable=False)
    contract = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    name = Column(String, nullable=False)
    number = Column(String, unique=True, index=True)
    main_executor = Column(Integer, ForeignKey("web_user.id"), nullable=False)
    deadline = Column(Date)
    status = Column(Integer, ForeignKey("project_statuses.id"), nullable=False)
    notes = Column(Text)

    object_info = relationship("Objects", back_populates="projects")
    contract_info = relationship("Contracts", back_populates="projects")
    executor_info = relationship(
        "Users", back_populates="projects", foreign_keys=[main_executor]
    )

    project_info = relationship("ProjectStatuses", back_populates="projects")


@event.listens_for(Projects, "before_insert")
def before_insert_listener(mapper, connection, target):
    if not target.number and target.objects:
        target.number = generate_project_number(target.objects)
