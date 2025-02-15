from pydantic import BaseModel
from pydantic import Field, constr
from web_app.schemas.users import UserResponse




# Schema
class ProjectExecutorsCreate(BaseModel):
    user: UserResponse
    #project:!!!!!

class ProjectExecutorsResponse(BaseModel):
    id: int
    user: UserResponse
    #project: !!!!

    class Config:
        orm_mode = True
