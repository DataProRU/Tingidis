from datetime import date

from fastapi import HTTPException, APIRouter, Depends, status, Query
from typing import Annotated, Optional, List

from sqlalchemy import and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from web_app.database import get_db
from sqlalchemy.future import select

from web_app.models import ProjectExecutors, Projects, Users
from web_app.schemas.project_executors import (
    ProjectExecutorsGetResponse,
    ProjectExecutorsResponse,
    ProjectExecutorsCreate,
    ProjectExecutorsUpdate,
)
from web_app.middlewares.auth_middleware import token_verification_dependency

from web_app.utils.logs import log_action

router = APIRouter()


# Endpoints


@router.get("/project-executors", response_model=list[ProjectExecutorsGetResponse])
async def get_project_executors(
    db: AsyncSession = Depends(get_db),
    user_full_name: Annotated[list[str] | None, Query()] = None,
    user_position: Annotated[list[str] | None, Query()] = None,
    user_email: Annotated[list[str] | None, Query()] = None,
    user_specialization: Annotated[list[str] | None, Query()] = None,
    project_name: Annotated[list[str] | None, Query()] = None,
    project_number: Annotated[list[str] | None, Query()] = None,
    project_status: Annotated[list[int] | None, Query()] = None,
    project_deadline: Annotated[list[date] | None, Query()] = None,
    user_data: dict = Depends(token_verification_dependency),
    sortBy: Optional[str] = None,
    sortDir: Optional[str] = "asc",
):
    join_user = sortBy in [
        "user_full_name",
        "user_position",
        "user_email",
        "user_specialization",
    ] or bool(user_full_name or user_position or user_email or user_specialization)
    join_project = sortBy in [
        "project_name",
        "project_number",
        "project_status",
        "project_deadline",
    ] or bool(project_name or project_number or project_status or project_deadline)

    stmt = select(ProjectExecutors)

    if join_user:
        stmt = stmt.join(ProjectExecutors.user_info)
    if join_project:
        stmt = stmt.join(ProjectExecutors.project_info)

    stmt = stmt.options(
        selectinload(ProjectExecutors.project_info),
        selectinload(ProjectExecutors.user_info),
    )

    filters = []

    if user_full_name:
        if not join_user:
            stmt = stmt.join(ProjectExecutors.user_info)
        filters.append(
            or_(
                or_(
                    Users.full_name.ilike(f"%{name}%"),
                    Users.first_name.ilike(f"%{name}%"),
                    Users.last_name.ilike(f"%{name}%"),
                )
                for name in user_full_name
            )
        )
    if user_position:
        if not join_user:
            stmt = stmt.join(ProjectExecutors.user_info)
        filters.append(or_(Users.position.ilike(f"%{pos}%") for pos in user_position))
    if user_email:
        if not join_user:
            stmt = stmt.join(ProjectExecutors.user_info)
        filters.append(or_(Users.email.ilike(f"%{email}%") for email in user_email))
    if user_specialization:
        if not join_user:
            stmt = stmt.join(ProjectExecutors.user_info)
        filters.append(
            or_(Users.specialization.ilike(f"%{spec}%") for spec in user_specialization)
        )

    if project_name:
        if not join_project:
            stmt = stmt.join(ProjectExecutors.project_info)
        filters.append(or_(Projects.name.ilike(f"%{name}%") for name in project_name))
    if project_number:
        if not join_project:
            stmt = stmt.join(ProjectExecutors.project_info)
        filters.append(or_(Projects.number.ilike(f"%{num}%") for num in project_number))
    if project_status:
        if not join_project:
            stmt = stmt.join(ProjectExecutors.project_info)
        filters.append(Projects.status.in_(project_status))
    if project_deadline:
        if not join_project:
            stmt = stmt.join(ProjectExecutors.project_info)
        filters.append(Projects.deadline.in_(project_deadline))

    if filters:
        stmt = stmt.where(and_(*filters))

    if sortBy:
        if sortBy == "user_full_name":
            if not join_user:
                stmt = stmt.join(ProjectExecutors.user_info)
            sort_column = Users.full_name
        elif sortBy == "user_position":
            if not join_user:
                stmt = stmt.join(ProjectExecutors.user_info)
            sort_column = Users.position
        elif sortBy == "user_email":
            if not join_user:
                stmt = stmt.join(ProjectExecutors.user_info)
            sort_column = Users.email
        elif sortBy == "user_specialization":
            if not join_user:
                stmt = stmt.join(ProjectExecutors.user_info)
            sort_column = Users.specialization
        elif sortBy == "project_name":
            if not join_project:
                stmt = stmt.join(ProjectExecutors.project_info)
            sort_column = Projects.name
        elif sortBy == "project_number":
            if not join_project:
                stmt = stmt.join(ProjectExecutors.project_info)
            sort_column = Projects.number
        elif sortBy == "project_status":
            if not join_project:
                stmt = stmt.join(ProjectExecutors.project_info)
            sort_column = Projects.status
        elif sortBy == "project_deadline":
            if not join_project:
                stmt = stmt.join(ProjectExecutors.project_info)
            sort_column = Projects.deadline
        else:
            try:
                sort_column = getattr(ProjectExecutors, sortBy)
            except AttributeError:
                raise HTTPException(
                    status_code=404, detail=f"Поле '{sortBy}' не найдено"
                )

        # Применяем направление сортировки
        if sortDir.lower() == "desc":
            stmt = stmt.order_by(sort_column.desc())
        else:
            stmt = stmt.order_by(sort_column.asc())

    result = await db.execute(stmt)
    projects_executors = result.scalars().all()

    response = []
    for projects_executor in projects_executors:
        response.append(
            {
                "id": projects_executor.id,
                "user": (
                    {
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
                        "notification": projects_executor.user_info.notification,
                    }
                    if projects_executor.user_info
                    else None
                ),
                "project": (
                    {
                        "id": projects_executor.project_info.id,
                        "object": projects_executor.project_info.object,
                        "contract": projects_executor.project_info.contract,
                        "name": projects_executor.project_info.name,
                        "number": projects_executor.project_info.number,
                        "main_executor": projects_executor.project_info.main_executor,
                        "deadline": projects_executor.project_info.deadline,
                        "status": projects_executor.project_info.status,
                        "notes": projects_executor.project_info.notes,
                    }
                    if projects_executor.project_info
                    else None
                ),
            }
        )

    return response


@router.get(
    "/project-executors/{project_executor_id}",
    response_model=ProjectExecutorsGetResponse,
)
async def get_project_executor_by_id(
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
            "notification": project_executor.user_info.notification,
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
async def create_project_executor(
    project_executor_data: ProjectExecutorsCreate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    existing_executor = await db.execute(
        select(ProjectExecutors).where(
            ProjectExecutors.user == project_executor_data.user,
            ProjectExecutors.project == project_executor_data.project,
        )
    )
    if existing_executor.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Исполнитель уже добавлен на проект",
        )

    project = await db.execute(
        select(Projects).where(Projects.id == project_executor_data.project)
    )
    project = project.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Проект не найден",
        )

    if project_executor_data.user == project.main_executor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Исполнитель не может быть основным ответственным за проект",
        )

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
async def update_project_executor(
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

    project = await db.execute(
        select(Projects).where(Projects.id == project_executor.project)
    )
    project = project.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Проект не найден",
        )

    if object_data.user and object_data.user == project.main_executor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Исполнитель не может быть основным ответственным за проект",
        )

    if object_data.user and object_data.project:
        existing_executor = await db.execute(
            select(ProjectExecutors).where(
                ProjectExecutors.user == object_data.user,
                ProjectExecutors.project == object_data.project,
                ProjectExecutors.id != project_executor_id,
            )
        )
        if existing_executor.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Исполнитель уже добавлен на проект",
            )

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
            "notification": project_executor.user_info.notification,
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
async def delete_project_executor(
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
