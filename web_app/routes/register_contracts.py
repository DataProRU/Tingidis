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
        stmt = select(Contract)
        result = await db.execute(stmt)
        contracts = result.scalars().all()
        logo_file = get_logo()
        bg_file = get_bg()

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


@router.post("/users/{user_id}/edit/")
async def update_user(
    contract_id: int,
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
    form_data = await request.form()
    logger.info(f"Form data received: {form_data}")
    if isinstance(user, RedirectResponse):
        logger.warning("Unauthenticated user access attempt")
        return user  # If the user is not authenticated

    try:
        stmt = select(Contract).where(Contract.id == contract_id)
        result = await db.execute(stmt)
        contract = result.scalar_one_or_none()

        if not user:
            logger.error(f"Contract not found: {contract_id}")
            return JSONResponse({"detail": "Contract not found"}, status_code=404)

        # Обновляем данные пользователя
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
        logger.info(f"User {contract_id} updated successfully")
        return RedirectResponse(url="/register_contracts/", status_code=303)

    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error: {e}")
        return JSONResponse({"detail": str(e)}, status_code=500)


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
        logger.info(f"New contract added: {new_contract.contract_code}")
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
    logger.info(f"Fetching user details for user_id: {contract_id}")
    if isinstance(user, RedirectResponse):
        logger.warning("Unauthenticated user access attempt")
        return user  # If the user is not authenticated
    stmt = select(Contract).where(Contract.id == contract_id)
    result = await db.execute(stmt)
    contract = result.scalar_one_or_none()

    if not user:
        logger.error(f"User not found: {contract_id}")
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
            "date_start": contract.date_start,
            "date_finish": contract.date_finish,
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
        stmt = select(Contract).where(Contract.id == contract_id)
        result = await db.execute(stmt)
        contract = result.scalar_one_or_none()

        if not user:
            logger.error(f"User not found: {contract_id}")
            return templates.TemplateResponse("not_found.html", {"request": Request()})

        await db.delete(contract)
        await db.commit()
        logger.info(f"Contract {contract_id} deleted successfully")

        return RedirectResponse(url="/register_contracts/", status_code=303)
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error: {e}")
        return JSONResponse(
            {"detail": "Database error"},
            status_code=505,
        )
