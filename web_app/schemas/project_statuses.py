from pydantic import BaseModel
from pydantic import Field, constr


# Schema
class ProjectStatusCreate(BaseModel):
    name: constr(min_length=1, max_length=30)


class ProjectStatusResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
