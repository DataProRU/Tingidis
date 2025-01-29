from pydantic import BaseModel
from pydantic import Field, constr


# Schema
class PersonContractCreate(BaseModel):
    first_name: constr(min_length=1, max_length=6)
    last_name: constr(min_length=1, max_length=30)
    father_name: constr(min_length=1, max_length=30)

    email: constr(min_length=1, max_length=30)
    position: constr(min_length=1, max_length=30)

    customer: int


class PersonContractResponse(BaseModel):
    id: int

    first_name: str
    last_name: str
    father_name: str

    email: str
    position: str

    customer: int

    class Config:
        orm_mode = True
