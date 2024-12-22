import logging
from fastapi import APIRouter, Request, Form, Depends, status
from web_app.database import Contract, get_db
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from web_app.services.storage import get_bg, get_logo
from web_app.services.contracts_services import (
    get_all_contracts,
    update_contract,
    add_new_contract,
    service_delete_contract,
)
from web_app.dependencies import get_authenticated_user
from datetime import date

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="web_app/templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/register_contracts/")
async def get_contracts(
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_authenticated_user),
):
    logger.info("Accessing contracts registration page")
    if isinstance(user, RedirectResponse):
        logger.warning("Unauthenticated user access attempt")
        return user  # Если пользователь не аутентифицирован

    try:
        contracts = await get_all_contracts(db)
        logo_file = await get_logo()
        bg_file = await get_bg()

        return templates.TemplateResponse(
            "register_contracts.html",
            {
                "request": request,
                "contracts": contracts,
                "bg_filename": bg_file,
                "logo_file": logo_file,
            },
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        return JSONResponse(
            {"detail": "Database error"},
            status_code=500,
        )


@router.post("/register_contracts/{contract_id}/edit/")
async def edit_contract(
    contract_id: int,
    contract_code: int = Form(...),
    object_name: str = Form(...),
    customer: str = Form(...),
    executer: str = Form(...),
    contract_number: int = Form(...),
    status: str = Form(...),
    stage: str = Form(...),
    contract_scan: str = Form(...),
    original_scan: str = Form(...),
    percent_complite: int = Form(...),
    date_start: date = Form(...),
    date_finish: date = Form(...),
    cost: int = Form(...),
    money_received: int = Form(...),
    money_left: int = Form(...),
    scan_complited_act: str = Form(...),
    original_complited_act: str = Form(...),
    volumes: str = Form(...),
    notes: str = Form(...),
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_authenticated_user),
):
    logger.info(f"Editing contract with ID: {contract_id}")
    if isinstance(user, RedirectResponse):
        logger.warning("Unauthenticated user access attempt")
        return user  # If the user is not authenticated
    try:
        await update_contract(
            contract_id,
            db,
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
        logger.info(f"Contract with ID {contract_id} updated successfully by route")
        return RedirectResponse(url="/register_contracts/", status_code=303)

    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error: {e}")
        return JSONResponse(
            {"detail": "Database error"},
            status_code=500,
        )


@router.post("/register_contracts/add/")
async def add_contract(
    request: Request,
    contract_code: int = Form(...),
    object_name: str = Form(...),
    customer: str = Form(...),
    executer: str = Form(...),
    contract_number: int = Form(...),
    status: str = Form(...),
    stage: str = Form(...),
    contract_scan: str = Form(...),
    original_scan: str = Form(...),
    percent_complite: int = Form(...),
    date_start: date = Form(...),
    date_finish: date = Form(...),
    cost: int = Form(...),
    money_received: int = Form(...),
    money_left: int = Form(...),
    scan_complited_act: str = Form(...),
    original_complited_act: str = Form(...),
    volumes: str = Form(...),
    notes: str = Form(...),
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_authenticated_user),
):
    logger.warning("open")
    if isinstance(user, RedirectResponse):
        logger.warning("Unauthenticated user access attempt")
        return user  # If the user is not authenticated
    try:
        await add_new_contract(
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
            db=db,
        )
        logger.info(f"New contract added in router")
        return RedirectResponse(url="/register_contracts/", status_code=303)

    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error: {e}")
        return JSONResponse(
            {"detail": "Database error"},
            status_code=500,
        )


@router.get("/register_contracts/{contract_id}/")
async def get_contract(
    contract_id: int,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_authenticated_user),
):
    logger.info(f"Fetching contract details for contract_id: {contract_id}")
    if isinstance(user, RedirectResponse):
        logger.warning("Unauthenticated user access attempt")
        return user  # If the user is not authenticated
    stmt = select(Contract).where(Contract.id == contract_id)
    result = await db.execute(stmt)
    contract = result.scalar_one_or_none()

    if not contract:
        logger.error(f"Contract not found: {contract_id}")
        return JSONResponse({"detail": "Contract not found"}, status_code=404)

    return JSONResponse(
        {
            "id": contract.id,
            "contract_code": contract.contract_code,
            "object_name": contract.object_name,
            "customer": contract.customer,
            "executer": contract.executer,
            "contract_number": contract.contract_number,
            "status": contract.status,
            "stage": contract.stage,
            "contract_scan": contract.contract_scan,
            "original_scan": contract.original_scan,
            "percent_complite": contract.percent_complite,
            "date_start": (
                contract.date_start.isoformat() if contract.date_start else None
            ),
            "date_finish": (
                contract.date_finish.isoformat() if contract.date_finish else None
            ),
            "cost": contract.cost,
            "money_received": contract.money_received,
            "money_left": contract.money_left,
            "scan_complited_act": contract.scan_complited_act,
            "original_complited_act": contract.original_complited_act,
            "volumes": contract.volumes,
            "notes": contract.notes,
        }
    )


@router.post("/register_contracts/{contract_id}/delete/")
async def delete_contract(
    contract_id: int,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_authenticated_user),
):
    if isinstance(user, RedirectResponse):
        logger.warning("Unauthenticated user access attempt")
        return user  # If the user is not authenticated
    logger.info(f"Deleting user with user_id: {contract_id}")
    try:
        await service_delete_contract(contract_id, db)
        logger.info(f"Contract {contract_id} deleted successfully")

        return RedirectResponse(url="/register_contracts/", status_code=303)
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error: {e}")
        return JSONResponse(
            {"detail": "Database error"},
            status_code=505,
        )
