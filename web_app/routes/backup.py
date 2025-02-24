from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from web_app.database import get_db
from web_app.middlewares.auth_middleware import token_verification_dependency

from web_app.utils.reports import generate_excel_report

router = APIRouter()


@router.get("/export", response_class=Response)
async def export_to_excel(
    db: AsyncSession = Depends(get_db),
    # user_data: dict = Depends(token_verification_dependency),
):
    # Генерируем Excel-файл
    excel_file = await generate_excel_report(db)

    # Возвращаем файл как ответ
    headers = {"Content-Disposition": 'attachment; filename="report.xlsx"'}
    return Response(
        content=excel_file.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )
