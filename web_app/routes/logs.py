from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db
from .models import LogEntry

router = APIRouter()

@router.get("/logs")
async def get_logs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(LogEntry.__table__.select())
    logs = result.fetchall()
    return [{"datetime": log.datetime, "user": log.user, "action": log.action} for log in logs]