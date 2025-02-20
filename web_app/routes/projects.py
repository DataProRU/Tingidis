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
    )
    result = await db.execute(stmt)
    projects = result.scalars().all()

    response = []
    for project in projects:
        response.append(
            {
                "id": project.id,
                "object": {
                    "id": project.object.id,
                    "code": project.object.code,
                    "name": project.object.name,
                    "comment": project.object.comment,
                },
                "contract": {
                    "id": project.contract.id,
                    "first_name": project.contract.first_name,
                    "last_name": project.contract.last_name,
                    "father_name": project.contract.father_name,
                    "phone": project.contract.phone,
                    "email": project.contract.email,
                    "position": project.contract.position,
                    "customer": project.contract.customer.id,
                },
                "name": project.name,
                "number": project.number,
                "project_executors": [
                    {
                        "id": project.project_executors.id,
                        "first_name": project.project_executor.first_name,
                        "last_name": project.project_executor.last_name,
                        "father_name": project.project_executor.father_name,
                        "full_name": project.project_executor.full_name,
                        "position": project.project_executor.position,
                        "phone": project.project_executor.phone,
                        "email": project.project_executor.email,
                        "telegram": project.project_executor.telegram,
                        "birthday": project.project_executor.birthday,
                        "category": project.project_executor.category,
                        "specialization": project.project_executor.specialization,
                        "username": project.project_executor.username,
                        "password": None,
                        "notes": project.project_executor.notes,
                        "role": project.project_executor.role,
                    }
                ],
                "deadline": project.deadline,
                "status": {"id": project.status.id, "name": project.status.name},
                "notes": project.notes,
            }
        )

    return response


@router.get("/projects/{project_id}", response_model=ProjectGetResponse)
async def get_project_by_id(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    # user_data: dict = Depends(token_verification_dependency),
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

    return {
        "id": project.id,
        "object": {"id": 0, "code": "string", "name": "string", "comment": "string"},
        "contract": {
            "id": 0,
            "first_name": "string",
            "last_name": "string",
            "father_name": "string",
            "phone": "string",
            "email": "string",
            "position": "string",
            "customer": 0,
        },
        "name": project.name,
        "number": project.number,
        "project_executors": [
            {
                "id": project.project_executors.id,
                "first_name": project.project_executor.first_name,
                "last_name": project.project_executor.last_name,
                "father_name": project.project_executor.father_name,
                "full_name": project.project_executor.full_name,
                "position": project.project_executor.position,
                "phone": project.project_executor.phone,
                "email": project.project_executor.email,
                "telegram": project.project_executor.telegram,
                "birthday": project.project_executor.birthday,
                "category": project.project_executor.category,
                "specialization": project.project_executor.specialization,
                "username": project.project_executor.username,
                "password": None,
                "notes": project.project_executor.notes,
                "role": project.project_executor.role,
            }
        ],
        "deadline": project.deadline,
        "status": {"id": project.status.id, "name": project.status.name},
        "notes": project.notes,
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
