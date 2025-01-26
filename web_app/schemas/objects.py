from pydantic import BaseModel
from pydantic import Field, constr
from typing import Optional


# Schema
class ObjectCreate(BaseModel):
    code: constr(min_length=1, max_length=6)
    name: constr(min_length=1, max_length=30)
    comment: Optional[str] = None


class ObjectResponse(BaseModel):
    id: int
    code: str
    name: str
    comment: Optional[str]

    class Config:
        orm_mode = True
