from fastapi import HTTPException, APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from web_app.database import get_db
from sqlalchemy.future import select
from web_app.models.projects import Projects
from web_app.schemas.projects import (
    ProjectResponse,
    ProjectUpdate,
    ProjectGetResponse,
    ProjectCreateResponse,
)
from web_app.middlewares.auth_middleware import token_verification_dependency

from web_app.utils.utils import log_action

router = APIRouter()


# Endpoints
@router.get("/projects", response_model=List[ProjectGetResponse])
async def get_projects(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    stmt = select(Projects).options(
        selectinload(Projects.object_info),
        selectinload(Projects.contract_info),
        selectinload(Projects.executor_info),
        selectinload(Projects.project_info),
        selectinload(Projects.project_executors),
    )
    result = await db.execute(stmt)
    projects = result.scalars().all()

    response = []
    for project in projects:
        response.append(
            {
                "id": project.id,
                "object": {
                    "id": project.object_info.id,
                    "code": project.object_info.code,
                    "name": project.object_info.name,
                    "comment": project.object_info.comment,
                },
                "contract": {
                    "id": project.contract_info.id,
                    "first_name": project.contract_info.executor_info.first_name,
                    "last_name": project.contract_info.executor_info.last_name,
                    "father_name": project.contract_info.executor_info.father_name,
                    "phone": project.contract_info.executor_info.phone,
                    "email": project.contract_info.executor_info.email,
                    "position": project.contract_info.executor_info.position,
                    "customer": project.contract_info.customer,
                },
                "name": project.name,
                "number": project.number,
                "project_main_executor": {
                    "id": project.executor_info.id,
                    "first_name": project.executor_info.first_name,
                    "last_name": project.executor_info.last_name,
                    "father_name": project.executor_info.father_name,
                    "full_name": project.executor_info.full_name,
                    "position": project.executor_info.position,
                    "phone": project.executor_info.phone,
                    "email": project.executor_info.email,
                    "telegram": project.executor_info.telegram,
                    "birthday": project.executor_info.birthday,
                    "category": project.executor_info.category,
                    "specialization": project.executor_info.specialization,
                    "username": project.executor_info.username,
                    "password": None,
                    "notes": project.executor_info.notes,
                    "role": project.executor_info.role,
                },
                "deadline": project.deadline,
                "status": {
                    "id": project.project_info.id,
                    "name": project.project_info.name,
                },
                "notes": project.notes,
                "project_executors": [
                    {
                        "id": executor.id,
                        "first_name": executor.first_name,
                        "last_name": executor.last_name,
                        "father_name": executor.father_name,
                        "full_name": executor.full_name,
                        "position": executor.position,
                        "phone": executor.phone,
                        "email": executor.email,
                        "telegram": executor.telegram,
                        "birthday": executor.birthday,
                        "category": executor.category,
                        "specialization": executor.specialization,
                        "username": executor.username,
                        "password": None,
                        "notes": executor.notes,
                        "role": executor.role,
                    }
                    for executor in project.project_executors
                ],
            }
        )

    return response


@router.get("/projects/{project_id}", response_model=ProjectGetResponse)
async def get_project_by_id(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(Projects)
        .options(
            selectinload(Projects.object_info),
            selectinload(Projects.contract_info),
            selectinload(Projects.executor_info),
            selectinload(Projects.project_info),
            selectinload(Projects.project_executors),
        )
        .filter(Projects.id == project_id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")

    return {
        "object": {
            "id": project.object_info.id,
            "code": project.object_info.code,
            "name": project.object_info.name,
            "comment": project.object_info.comment,
        },
        "contract": {
            "id": project.contract_info.id,
            "first_name": project.contract_info.executor_info.first_name or "",
            "last_name": project.contract_info.executor_info.last_name or "",
            "father_name": project.contract_info.executor_info.father_name or "",
            "phone": project.contract_info.executor_info.phone or "",
            "email": project.contract_info.executor_info.email or "",
            "position": project.contract_info.executor_info.position or "",
            "customer": project.contract_info.customer,
        },
        "name": project.name,
        "number": project.number,
        "project_main_executor": {
            "id": project.executor_info.id,
            "first_name": project.executor_info.first_name,
            "last_name": project.executor_info.last_name,
            "father_name": project.executor_info.father_name,
            "full_name": project.executor_info.full_name,
            "position": project.executor_info.position,
            "phone": project.executor_info.phone,
            "email": project.executor_info.email,
            "telegram": project.executor_info.telegram,
            "birthday": project.executor_info.birthday,
            "category": project.executor_info.category,
            "specialization": project.executor_info.specialization,
            "username": project.executor_info.username,
            "password": None,
            "notes": project.executor_info.notes,
            "role": project.executor_info.role,
        },
        "deadline": project.deadline,
        "status": {"id": project.project_info.id, "name": project.project_info.name},
        "notes": project.notes,
        "project_executors": [
            {
                "id": executor.id,
                "first_name": executor.first_name,
                "last_name": executor.last_name,
                "father_name": executor.father_name,
                "full_name": executor.full_name,
                "position": executor.position,
                "phone": executor.phone,
                "email": executor.email,
                "telegram": executor.telegram,
                "birthday": executor.birthday,
                "category": executor.category,
                "specialization": executor.specialization,
                "username": executor.username,
                "password": None,
                "notes": executor.notes,
                "role": executor.role,
            }
            for executor in project.project_executors
        ],
    }


@router.post(
    "/projects",
    response_model=ProjectCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
@log_action("Создание проекта")
async def create_project(
    project_data: ProjectCreateResponse,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    project = Projects(**project_data.dict())
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


@router.patch("/projects/{project_id}", response_model=ProjectGetResponse)
@log_action("Обновление проекта")
async def update_project(
    project_id: int,
    object_data: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(Projects)
        .options(
            selectinload(Projects.object_info),
            selectinload(Projects.contract_info),
            selectinload(Projects.executor_info),
            selectinload(Projects.project_info),
        )
        .filter(Projects.id == project_id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")

    for key, value in object_data.dict(exclude_unset=True).items():
        setattr(project, key, value)

    await db.commit()
    await db.refresh(project)
    return {
        "id": project.id,
        "objects": {
            "id": project.objects.id,
            "code": project.objects.code,
            "name": project.objects.name,
            "comment": project.objects.comment,
        },
        "contracts": {
            "id": project.contracts.id,
            "first_name": project.contracts.first_name,
            "last_name": project.contracts.last_name,
            "father_name": project.contracts.father_name,
            "phone": project.contracts.phone,
            "email": project.contracts.email,
            "position": project.contracts.position,
            "customer": project.contracts.customer,
        },
        "name": project.name,
        "number": project.number,
        "main_executor": {
            "id": project.main_executor.id,
            "first_name": project.main_executor.first_name,
            "last_name": project.main_executor.last_name,
            "father_name": project.main_executor.father_name,
            "full_name": project.main_executor.full_name,
            "position": project.main_executor.position,
            "phone": project.main_executor.phone,
            "email": project.main_executor.email,
            "telegram": project.main_executor.telegram,
            "birthday": project.main_executor.birthday,
            "category": project.main_executor.category,
            "specialization": project.main_executor.specialization,
            "username": project.main_executor.username,
            "password": None,
            "notes": project.main_executor.notes,
            "role": project.main_executor.role,
        },
        "deadline": project.deadline,
        "status": {"id": project.status.id, "name": project.status.name},
        "notes": project.notes,
    }


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    # Проверка наличия объекта
    result = await db.execute(select(Projects).filter(Projects.id == project_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Проект не найден")

    # Удаление объекта
    await db.delete(obj)
    await db.commit()
    return {
        "message": "Контакт успешно удален",
        "project_id": project_id,
    }
