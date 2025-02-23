from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import date

from web_app.schemas.objects import ObjectResponse
from web_app.schemas.contracts import ContractsResponse, ContractsGetResponse
from web_app.schemas.users import UserResponse
from web_app.schemas.project_statuses import ProjectStatusResponse


class ProjectGetResponse(BaseModel):
    id: Optional[int] = None
    object: ObjectResponse
    contract: Optional[ContractsResponse] = None
    name: str
    number: str
    main_executor: UserResponse
    deadline: date
    status: ProjectStatusResponse
    notes: Optional[str] = None
    project_executors: List["ProjectExecutorsGetResponse"]

    class Config:
        orm_mode = True


class ProjectCreateResponse(BaseModel):
    object: int
    contract: Optional[int] = None
    name: str
    number: str
    main_executor: int
    deadline: date
    status: int
    notes: Optional[str] = None

    class Config:
        orm_mode = True


class ProjectResponse(BaseModel):
    id: Optional[int] = None
    object: int
    contract: Optional[int] = None
    name: str
    number: str
    main_executor: int
    deadline: date
    status: int
    notes: Optional[str] = None

    class Config:
        orm_mode = True


class ProjectUpdate(BaseModel):
    object: Optional[int] = None
    contract: Optional[int] = None
    name: Optional[str] = None
    number: Optional[str] = None
    main_executor: Optional[int] = None
    deadline: Optional[date] = None
    status: Optional[int] = None
    notes: Optional[str] = None

    class Config:
        orm_mode = True


# Отложенный импорт
from web_app.schemas.project_executors import ProjectExecutorsGetResponse

ProjectGetResponse.update_forward_refs()
