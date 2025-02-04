from pydantic import BaseModel, constr
from typing import Optional, List


class CustomerGetResponse(BaseModel):
    id: Optional[int] = None
    form: "FormOfOwnershipResponse"
    name: str
    address: str
    inn: str
    notes: Optional[str] = None
    contacts: List["ContactResponse"]

    class Config:
        orm_mode = True


class CustomerCreateResponse(BaseModel):
    id: Optional[int] = None
    form: int
    name: str
    address: str
    inn: str
    notes: Optional[str] = None
    contacts: Optional[List["ContactCreateResponse"]] = None


class CustomerResponse(BaseModel):
    id: Optional[int] = None
    form: int
    name: str
    address: str
    inn: str
    notes: Optional[str] = None


class CustomerUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=255)] = None
    form: Optional[int] = None
    address: Optional[constr(min_length=1, max_length=255)] = None
    inn: Optional[constr(min_length=1, max_length=255)] = None
    notes: Optional[str] = None


from web_app.schemas.contacts import ContactResponse, ContactCreateResponse
from web_app.schemas.form_of_ownership import FormOfOwnershipResponse

CustomerGetResponse.update_forward_refs()
