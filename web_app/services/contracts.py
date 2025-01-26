# from web_app.schemas.contracts import ContractsModel
# from web_app.database import get_db
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from fastapi import Depends
# import logging
# from web_app.schemas.contracts import ContractUpdate, ContractCreate
#
#
# logger = logging.getLogger(__name__)
#
#
# async def get_all_contracts(db: AsyncSession = Depends(get_db)) -> list:
#     stmt = select(Contract)
#     result = await db.execute(stmt)
#     contracts = result.scalars().all()
#     return contracts
#
#
# async def get_contract_by_id(contract_id: int, db: AsyncSession) -> Contract | None:
#     stmt = select(Contract).where(Contract.id == contract_id)
#     result = await db.execute(stmt)
#     contract = result.scalar_one_or_none()
#     if not contract:
#         logger.error(f"Contract not found: {contract_id}")
#         return None
#     return contract
#
#
# async def edit_contract(
#     contract_id: int,
#     db: AsyncSession,
#     contract_data: ContractUpdate,
# ) -> None:
#     contract = await get_contract_by_id(contract_id, db)
#     if not contract:
#         logger.error(f"Contract not found: {contract_id}")
#         return None
#
#     for key, value in contract_data.dict(exclude_unset=True).items():
#         setattr(contract, key, value)
#
#     await db.commit()
#     await db.refresh(contract)
#     logger.info(f"Contract with ID {contract_id} updated successfully by service")
#     return None
#
#
# async def add_contract(
#     contract_data: ContractCreate,
#     db: AsyncSession,
# ) -> None:
#     new_contract = Contract(**contract_data.dict())
#     db.add(new_contract)
#     await db.commit()
#     await db.refresh(new_contract)
#     logger.info(f"New contract added: {new_contract.contract_code} in services")
#     return None
#
#
# async def delete_contract(contract_id: int, db: AsyncSession) -> None:
#     contract = await get_contract_by_id(contract_id, db)
#     if not contract:
#         logger.error(f"Contract not found: {contract_id}")
#         return None
#
#     await db.delete(contract)
#     await db.commit()
#     logger.info(f"Contract deleted: {contract_id} in services")
#     return None
