from fastapi import APIRouter, Request, Form, Depends
from web_app.database import Contract, get_db
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from web_app.services.storage import get_bg, get_logo
from web_app.dependencies import get_authenticated_user

router = APIRouter()
templates = Jinja2Templates(directory="web_app/templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/register_contracts/")
async def get_contracts(
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_authenticated_user),
):
    if isinstance(user, RedirectResponse):
        return user  # Если пользователь не аутентифицирован

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
