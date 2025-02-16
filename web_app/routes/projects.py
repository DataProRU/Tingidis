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
)
from web_app.middlewares.auth_middleware import token_verification_dependency

from web_app.utils.utils import log_action

router = APIRouter()


# Endpoints
@router.get("/projects", response_model=List[ProjectGetResponse])
async def get_contacts(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    stmt = select(Projects).options(
        selectinload(Projects.object_info),
        selectinload(Projects.cotract_info),
        selectinload(Projects.executor_info),
        selectinload(Projects.status_info),
    )
    result = await db.execute(stmt)
    projects = result.scalar_one_or_none()

    response = []
    for project in projects:
        response.append(
            {
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
        )

    return response


@router.get("/projects/{contact_id}", response_model=ProjectGetResponse)
async def get_contact_by_id(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(
        select(Projects)
        .options(
            selectinload(Projects.object_info),
            selectinload(Projects.cotract_info),
            selectinload(Projects.executor_info),
            selectinload(Projects.status_info),
        )
        .filter(Projects.id == contact_id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")

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


@router.post(
    "/projects",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
@log_action("Создание контакта")
async def create_contact(
    contact_data: ProjectResponse,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    obj = Contacts(**contact_data.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


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
            selectinload(Projects.cotract_info),
            selectinload(Projects.executor_info),
            selectinload(Projects.status_info),
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
@log_action("Удаление проекта")
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
