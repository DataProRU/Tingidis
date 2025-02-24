from fastapi import HTTPException, APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from web_app.database import get_db
from sqlalchemy.future import select

from web_app.models import ProjectExecutors
from web_app.models.projects import Projects
from web_app.schemas.projects import (
    ProjectResponse,
    ProjectUpdate,
    ProjectGetResponse,
    ProjectCreateResponse,
)
from web_app.middlewares.auth_middleware import token_verification_dependency

from web_app.utils.logs import log_action

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
        selectinload(Projects.project_executors).selectinload(
            ProjectExecutors.user_info
        ),
        selectinload(Projects.project_executors).selectinload(
            ProjectExecutors.project_info
        ),
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
                "contract": (
                    {
                        "id": project.contract_info.id,
                        "code": project.contract_info.code,
                        "name": project.contract_info.name,
                        "customer": project.contract_info.customer,
                        "executor": project.contract_info.executor,
                        "number": project.contract_info.number,
                        "sign_date": project.contract_info.sign_date,
                        "price": project.contract_info.price,
                        "theme": project.contract_info.theme,
                        "evolution": project.contract_info.evolution,
                    }
                    if project.contract_info
                    else None
                ),
                "name": project.name,
                "number": project.number,
                "main_executor": {
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
                    "notification": project.executor_info.notification,
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
                        "user": {
                            **executor.user_info.__dict__,
                            "password": None,
                        },
                        "project": executor.project_info,
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
            selectinload(Projects.project_executors).selectinload(
                ProjectExecutors.user_info
            ),
            selectinload(Projects.project_executors).selectinload(
                ProjectExecutors.project_info
            ),
        )
        .filter(Projects.id == project_id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")

    return {
        "id": project.id,
        "object": {
            "id": project.object_info.id,
            "code": project.object_info.code,
            "name": project.object_info.name,
            "comment": project.object_info.comment,
        },
        "contract": (
            {
                "id": project.contract_info.id,
                "code": project.contract_info.code,
                "name": project.contract_info.name,
                "customer": project.contract_info.customer,
                "executor": project.contract_info.executor,
                "number": project.contract_info.number,
                "sign_date": project.contract_info.sign_date,
                "price": project.contract_info.price,
                "theme": project.contract_info.theme,
                "evolution": project.contract_info.evolution,
            }
            if project.contract_info
            else None
        ),
        "name": project.name,
        "number": project.number,
        "main_executor": {
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
            "notification": project.executor_info.notification,
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
                "user": {
                    **executor.user_info.__dict__,
                    "password": None,
                },
                "project": executor.project_info,
            }
            for executor in project.project_executors
        ],
    }


@router.post(
    "/projects",
    response_model=ProjectResponse,
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
            selectinload(Projects.project_executors),
            selectinload(Projects.project_executors).selectinload(
                ProjectExecutors.user_info
            ),
            selectinload(Projects.project_executors).selectinload(
                ProjectExecutors.project_info
            ),
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
        "object": {
            "id": project.object_info.id,
            "code": project.object_info.code,
            "name": project.object_info.name,
            "comment": project.object_info.comment,
        },
        "contract": (
            {
                "id": project.contract_info.id,
                "code": project.contract_info.code,
                "name": project.contract_info.name,
                "customer": project.contract_info.customer,
                "executor": project.contract_info.executor,
                "number": project.contract_info.number,
                "sign_date": project.contract_info.sign_date,
                "price": project.contract_info.price,
                "theme": project.contract_info.theme,
                "evolution": project.contract_info.evolution,
            }
            if project.contract_info
            else None
        ),
        "name": project.name,
        "number": project.number,
        "main_executor": {
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
            "notification": project.executor_info.notification,
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
                "user": {
                    **executor.user_info.__dict__,
                    "password": None,
                },
                "project": executor.project_info,
            }
            for executor in project.project_executors
        ],
    }


@router.delete("/projects/{object_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    object_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    # Проверка наличия объекта
    result = await db.execute(select(Projects).filter(Projects.id == object_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Проект не найден")

    # Удаление объекта
    await db.delete(obj)
    await db.commit()
    return {
        "message": "Контакт успешно удален",
        "project_id": object_id,
    }
