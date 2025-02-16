from typing import Optional

from pydantic import BaseModel

from web_app.schemas.users import UserResponse


# Schema
class ProjectExecutorsGetResponse(BaseModel):
    id: Optional[int] = None
    user: UserResponse
    project: "ProjectResponse"

    class Config:
        orm_mode = True


class ProjectExecutorsCreate(BaseModel):
    user: int
    project: int


class ProjectExecutorsResponse(BaseModel):
    id: Optional[int] = None
    user: int
    project: int

    class Config:
        orm_mode = True


class ProjectExecutorsUpdate(BaseModel):
    user: Optional[int] = None
    project: Optional[int] = None


from web_app.schemas.projects import ProjectResponse

ProjectResponse.update_forward_refs()
