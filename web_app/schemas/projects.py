from pydantic import BaseModel, constr
from typing import Optional
from datetime import date

from web_app.schemas.objects import ObjectResponse
from web_app.schemas.contacts import ContactResponse
from web_app.schemas.users import UserResponse
from web_app.schemas.project_statuses import ProjectStatusResponse


class ProjectGetResponse(BaseModel):
    id: Optional[int] = None
    objects: ObjectResponse
    contracts: ContactResponse
    name: str
    number: str
    main_executor: UserResponse
    deadline: date
    status: ProjectStatusResponse
    notes: str

    class Config:
        orm_mode = True


class ProjectCreateResponse(BaseModel):
    objects: ObjectResponse
    contracts: ContactResponse
    name: str
    number: str
    main_executor: UserResponse
    deadline: date
    status: ProjectStatusResponse
    notes: str

    class Config:
        orm_mode = True


class ProjectResponse(BaseModel):
    id: Optional[int] = None
    objects: ObjectResponse
    contracts: ContactResponse
    name: str
    number: str
    main_executor: UserResponse
    deadline: date
    status: ProjectStatusResponse
    notes: str

    class Config:
        orm_mode = True


class ProjectUpdate(BaseModel):
    objects: Optional[int] = None
    contracts: Optional[int] = None
    name: Optional[constr(min_length=1, max_length=50)] = None
    number: Optional[constr(min_length=1, max_length=50)] = None
    main_executor: Optional[int] = None
    deadline: Optional[constr(min_length=1, max_length=50)] = None
    status: Optional[int] = None
    notes: Optional[constr(min_length=1, max_length=50)] = None
