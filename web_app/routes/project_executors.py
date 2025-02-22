from fastapi import HTTPException, APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from web_app.database import get_db
from sqlalchemy.future import select

from web_app.models import ProjectExecutors
from web_app.schemas.project_executors import (
    ProjectExecutorsGetResponse,
    ProjectExecutorsResponse,
    ProjectExecutorsCreate,
    ProjectExecutorsUpdate,
)
from web_app.middlewares.auth_middleware import token_verification_dependency

from web_app.utils.utils import log_action

router = APIRouter()


# Endpoints
@router.get("/project-executors", response_model=List[ProjectExecutorsGetResponse])
async def get_project_executors(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    stmt = select(ProjectExecutors).options(
        selectinload(ProjectExecutors.project_info),
        selectinload(ProjectExecutors.user_info),
    )
    result = await db.execute(stmt)
    projects_executors = result.scalars().all()

    response = []
    for projects_executor in projects_executors:
        response.append(
            {
                "id": projects_executor.id,
                "user": {
                    "id": projects_executor.user_info.id,
                    "first_name": projects_executor.user_info.first_name,
                    "last_name": projects_executor.user_info.last_name,
                    "father_name": projects_executor.user_info.father_name,
                    "full_name": projects_executor.user_info.full_name,
                    "position": projects_executor.user_info.position,
                    "phone": projects_executor.user_info.phone,
                    "email": projects_executor.user_info.email,
                    "telegram": projects_executor.user_info.telegram,
                    "birthday": projects_executor.user_info.birthday,
                    "category": projects_executor.user_info.category,
                    "specialization": projects_executor.user_info.specialization,
                    "username": projects_executor.user_info.username,
                    "password": None,
                    "notes": projects_executor.user_info.notes,
                    "role": projects_executor.user_info.role,
                },
                "project": {
                    "id": projects_executor.project_info.id,
                    "object": projects_executor.project_info.object,
                    "contract": projects_executor.project_info.contract,
                    "name": projects_executor.project_info.name,
                    "number": projects_executor.project_info.number,
                    "main_executor": projects_executor.project_info.main_executor,
                    "deadline": projects_executor.project_info.deadline,
                    "status": projects_executor.project_info.status,
                    "notes": projects_executor.project_info.notes,
                },
            }
        )

    return response


@router.get(
    "/project-executors/{project_executor_id}",
    response_model=ProjectExecutorsGetResponse,
)
async def get_project_by_id(
    project_executor_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(ProjectExecutors)
        .options(
            selectinload(ProjectExecutors.project_info),
            selectinload(ProjectExecutors.user_info),
        )
        .filter(ProjectExecutors.id == project_executor_id)
    )
    project_executor = result.scalar_one_or_none()

    if not project_executor:
        raise HTTPException(status_code=404, detail="Исполнитель на проекте не найден")

    return {
        "id": project_executor.id,
        "user": {
            "id": project_executor.user_info.id,
            "first_name": project_executor.user_info.first_name,
            "last_name": project_executor.user_info.last_name,
            "father_name": project_executor.user_info.father_name,
            "full_name": project_executor.user_info.full_name,
            "position": project_executor.user_info.position,
            "phone": project_executor.user_info.phone,
            "email": project_executor.user_info.email,
            "telegram": project_executor.user_info.telegram,
            "birthday": project_executor.user_info.birthday,
            "category": project_executor.user_info.category,
            "specialization": project_executor.user_info.specialization,
            "username": project_executor.user_info.username,
            "password": None,
            "notes": project_executor.user_info.notes,
            "role": project_executor.user_info.role,
        },
        "project": {
            "id": project_executor.project_info.id,
            "object": project_executor.project_info.object,
            "contract": project_executor.project_info.contract,
            "name": project_executor.project_info.name,
            "number": project_executor.project_info.number,
            "main_executor": project_executor.project_info.main_executor,
            "deadline": project_executor.project_info.deadline,
            "status": project_executor.project_info.status,
            "notes": project_executor.project_info.notes,
        },
    }


@router.post(
    "/project-executors",
    response_model=ProjectExecutorsResponse,
    status_code=status.HTTP_201_CREATED,
)
@log_action("Добавление исполнителя на проекте")
async def create_project(
    project_executor_data: ProjectExecutorsCreate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    project_executor = ProjectExecutors(**project_executor_data.dict())
    db.add(project_executor)
    await db.commit()
    await db.refresh(project_executor)
    return project_executor


@router.patch(
    "/project-executors/{project_executor_id}",
    response_model=ProjectExecutorsGetResponse,
)
@log_action("Обновление исполнителя на проекте")
async def update_project(
    project_executor_id: int,
    object_data: ProjectExecutorsUpdate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(ProjectExecutors)
        .options(
            selectinload(ProjectExecutors.project_info),
            selectinload(ProjectExecutors.user_info),
        )
        .filter(ProjectExecutors.id == project_executor_id)
    )
    project_executor = result.scalar_one_or_none()
    if not project_executor:
        raise HTTPException(status_code=404, detail="Исполнитель на проекте не найден")

    for key, value in object_data.dict(exclude_unset=True).items():
        setattr(project_executor, key, value)

    await db.commit()
    await db.refresh(project_executor)
    return {
        "id": project_executor.id,
        "user": {
            "id": project_executor.user_info.id,
            "first_name": project_executor.user_info.first_name,
            "last_name": project_executor.user_info.last_name,
            "father_name": project_executor.user_info.father_name,
            "full_name": project_executor.user_info.full_name,
            "position": project_executor.user_info.position,
            "phone": project_executor.user_info.phone,
            "email": project_executor.user_info.email,
            "telegram": project_executor.user_info.telegram,
            "birthday": project_executor.user_info.birthday,
            "category": project_executor.user_info.category,
            "specialization": project_executor.user_info.specialization,
            "username": project_executor.user_info.username,
            "password": None,
            "notes": project_executor.user_info.notes,
            "role": project_executor.user_info.role,
        },
        "project": {
            "id": project_executor.project_info.id,
            "object": project_executor.project_info.object,
            "contract": project_executor.project_info.contract,
            "name": project_executor.project_info.name,
            "number": project_executor.project_info.number,
            "main_executor": project_executor.project_info.main_executor,
            "deadline": project_executor.project_info.deadline,
            "status": project_executor.project_info.status,
            "notes": project_executor.project_info.notes,
        },
    }


@router.delete("/project-executors/{object_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    object_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    # Проверка наличия объекта
    result = await db.execute(
        select(ProjectExecutors).filter(ProjectExecutors.id == object_id)
    )
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Исполнитель на проекте не найден")

    # Удаление объекта
    await db.delete(obj)
    await db.commit()
    return {
        "message": "Исполнитель на проекте успешно удален",
        "project_executor_id": object_id,
    }
