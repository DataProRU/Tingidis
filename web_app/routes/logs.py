from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc
from ..database import get_db
from ..middlewares.auth_middleware import token_verification_dependency
from ..models import LogEntry

router = APIRouter()


@router.get("/logs")
async def get_logs(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        LogEntry.__table__.select().order_by(desc(LogEntry.__table__.c.datetime))
    )
    logs = result.fetchall()

    return [
        {"datetime": log.datetime, "user": log.user, "action": log.action}
        for log in logs
    ]
