from fastapi import HTTPException, APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from web_app.database import get_db
from sqlalchemy.future import select
from web_app.models.project_statuses import ProjectStatuses
from web_app.schemas.project_statuses import ProjectStatusCreate, ProjectStatusResponse
from web_app.middlewares.auth_middleware import token_verification_dependency
from web_app.utils.logs import log_action

router = APIRouter()


# Endpoints
@router.get("/project-statuses", response_model=List[ProjectStatusResponse])
async def get_project_statuses(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    stmt = select(ProjectStatuses)
    result = await db.execute(stmt)
    project_statuses = result.scalars().all()
    return project_statuses


@router.get(
    "/project-statuses/{project_status_id}", response_model=ProjectStatusResponse
)
async def get_project_status_by_id(
    project_status_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(ProjectStatuses).filter(ProjectStatuses.id == project_status_id)
    )
    project_status = result.scalar_one_or_none()
    if not project_status:
        raise HTTPException(status_code=404, detail="Статус проекта не найден")
    return project_status


@router.post(
    "/project-statuses",
    response_model=ProjectStatusResponse,
    status_code=status.HTTP_201_CREATED,
)
@log_action("Создание статуса проекта в справочнике")
async def create_project_status(
    project_status_data: ProjectStatusCreate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    project_status = ProjectStatuses(**project_status_data.dict())
    db.add(project_status)
    await db.commit()
    await db.refresh(project_status)
    return project_status


@router.patch(
    "/project-statuses/{project_status_id}", response_model=ProjectStatusResponse
)
@log_action("Обновление статуса проекта в справочнике")
async def update_project_status(
    project_status_id: int,
    project_status_data: ProjectStatusCreate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(ProjectStatuses).filter(ProjectStatuses.id == project_status_id)
    )
    project_status = result.scalar_one_or_none()
    if not project_status:
        raise HTTPException(status_code=404, detail="Статус проекта не найден")

    for key, value in project_status_data.dict(exclude_unset=True).items():
        setattr(project_status, key, value)

    await db.commit()
    await db.refresh(project_status)
    return project_status


@router.delete("/project-statuses/{object_id}", status_code=status.HTTP_204_NO_CONTENT)
@log_action("Удаление статуса проекта в справочнике")
async def delete_project_status(
    object_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    # Проверка наличия объекта
    result = await db.execute(
        select(ProjectStatuses).filter(ProjectStatuses.id == object_id)
    )
    project_status = result.scalar_one_or_none()
    if not project_status:
        raise HTTPException(status_code=404, detail="Статус проекта не найден")

    # Удаление объекта
    await db.delete(project_status)
    await db.commit()
    return {
        "message": "Статус проекта успешно удалён",
        "object_id": object_id,
    }
