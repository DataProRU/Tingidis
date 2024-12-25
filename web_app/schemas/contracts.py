from pydantic import BaseModel, Field, constr
from datetime import date
from typing import Optional


class ContractCreate(BaseModel):
    contract_code: int
    object_name: str
    customer: str
    executer: str
    contract_number: str
    status: str
    stage: str
    contract_scan: str
    original_scan: str
    percent_complite: int
    date_start: date
    date_finish: Optional[date] = None
    cost: Optional[int] = None
    money_received: Optional[int] = None
    money_left: Optional[int] = None
    scan_complited_act: str
    original_complited_act: str
    volumes: str
    notes: Optional[str] = None


class ContractUpdate(BaseModel):
    contract_code: Optional[int] = None
    object_name: Optional[str] = None
    customer: Optional[str] = None
    executer: Optional[str] = None
    contract_number: Optional[str] = None
    status: Optional[str] = None
    stage: Optional[str] = None
    contract_scan: Optional[str] = None
    original_scan: Optional[str] = None
    percent_complite: Optional[int] = None
    date_start: Optional[date] = None
    date_finish: Optional[date] = None
    cost: Optional[int] = None
    money_received: Optional[int] = None
    money_left: Optional[int] = None
    scan_complited_act: Optional[str] = None
    original_complited_act: Optional[str] = None
    volumes: Optional[str] = None
    notes: Optional[str] = None
