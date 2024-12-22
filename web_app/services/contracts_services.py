from web_app.database import Contract, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends
from datetime import date
import logging


logger = logging.getLogger(__name__)


async def get_all_contracts(db: AsyncSession = Depends(get_db)) -> list:
    stmt = select(Contract)
    result = await db.execute(stmt)
    contracts = result.scalars().all()

    return contracts


async def get_contract_by_id(contract_id: int, db: AsyncSession) -> Contract | None:
    stmt = select(Contract).where(Contract.id == contract_id)
    result = await db.execute(stmt)
    contract = result.scalar_one_or_none()
    if not contract:
        logger.error(f"Contract not found: {contract_id}")
        return None
    return contract


async def update_contract(
    contract_id: int,
    db: AsyncSession,
    contract_code: int,
    object_name: str,
    customer: str,
    executer: str,
    contract_number: int,
    status: str,
    stage: str,
    contract_scan: str,
    original_scan: str,
    percent_complite: int,
    date_start: date,
    date_finish: date,
    cost: int,
    money_received: int,
    money_left: int,
    scan_complited_act: str,
    original_complited_act: str,
    volumes: str,
    notes: str,
) -> None:
    """Update a contract in the database."""
    contract = await get_contract_by_id(contract_id, db)
    if not contract:
        logger.error(f"Contract not found: {contract_id}")
        return None

    contract.contract_code = contract_code
    contract.object_name = object_name
    contract.customer = customer
    contract.executer = executer
    contract.contract_number = contract_number
    contract.status = status
    contract.stage = stage
    contract.contract_scan = contract_scan
    contract.original_scan = original_scan
    contract.percent_complite = percent_complite
    contract.date_start = date_start
    contract.date_finish = date_finish
    contract.cost = cost
    contract.money_received = money_received
    contract.money_left = money_left
    contract.scan_complited_act = scan_complited_act
    contract.original_complited_act = original_complited_act
    contract.volumes = volumes
    contract.notes = notes

    await db.commit()
    await db.refresh(contract)
    logger.info(f"Contract with ID {contract_id} updated successfully by service")

    return None


async def add_new_contract(
    contract_code: int,
    object_name: str,
    customer: str,
    executer: str,
    contract_number: int,
    status: str,
    stage: str,
    contract_scan: str,
    original_scan: str,
    percent_complite: int,
    date_start: date,
    date_finish: date,
    cost: int,
    money_received: int,
    money_left: int,
    scan_complited_act: str,
    original_complited_act: str,
    volumes: str,
    notes: str,
    db: AsyncSession,
) -> None:
    new_contract = Contract(
        contract_code=contract_code,
        object_name=object_name,
        customer=customer,
        executer=executer,
        contract_number=contract_number,
        status=status,
        stage=stage,
        contract_scan=contract_scan,
        original_scan=original_scan,
        percent_complite=percent_complite,
        date_start=date_start,
        date_finish=date_finish,
        cost=cost,
        money_received=money_received,
        money_left=money_left,
        scan_complited_act=scan_complited_act,
        original_complited_act=original_complited_act,
        volumes=volumes,
        notes=notes,
    )
    db.add(new_contract)
    await db.commit()
    await db.refresh(new_contract)
    logger.info(f"New contract added: {new_contract.contract_code} in services")
    return None


async def service_delete_contract(contract_id, db: AsyncSession) -> None:
    contract = await get_contract_by_id(contract_id, db)

    if not contract:
        logger.error(f"Contract not found: {contract_id}")

    await db.delete(contract)
    await db.commit()
    return None
