from datetime import date

from fastapi import HTTPException, APIRouter, Depends, status, Query
from typing import Annotated, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from web_app.database import get_db
from sqlalchemy.future import select

from web_app.models import (
    ProjectExecutors,
    Contracts,
    Objects,
    Customers,
    Users,
    ProjectStatuses,
)
from web_app.models.projects import Projects
from web_app.schemas.projects import (
    ProjectResponse,
    ProjectUpdate,
    ProjectGetResponse,
    ProjectCreateResponse,
)
from web_app.middlewares.auth_middleware import token_verification_dependency
from sqlalchemy import exc, or_, and_

from web_app.utils.logs import log_action

router = APIRouter()


# Endpoints


@router.get("/projects")
async def get_projects(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
    id: Annotated[list[int] | None, Query()] = None,
    number: Annotated[list[str] | None, Query()] = None,
    name: Annotated[list[str] | None, Query()] = None,
    object: Annotated[list[str] | None, Query()] = None,
    contract: Annotated[list[str] | None, Query()] = None,
    main_executor: Annotated[list[str] | None, Query()] = None,
    deadline: Annotated[list[date] | None, Query()] = None,
    status: Annotated[list[str] | None, Query()] = None,
    notes: Annotated[list[str] | None, Query()] = None,
    project_executor: Annotated[list[str] | None, Query()] = None,
    sortBy: Optional[str] = None,
    sortDir: Optional[str] = "asc",
):
    join_object = sortBy in ["object", "name"] or bool(object or name)
    join_contract = sortBy == "number" or bool(contract)
    join_main_executor = sortBy == "main_executor" or bool(main_executor)
    join_project_executor = sortBy == "project_executor" or bool(project_executor)
    join_status = sortBy == "status" or bool(status)

    stmt = select(Projects)

    if join_object:
        stmt = stmt.join(Projects.object_info)
    if join_contract:
        stmt = stmt.join(Projects.contract_info)
    if join_main_executor:
        stmt = stmt.join(Projects.executor_info)
    if join_project_executor:
        stmt = stmt.join(Projects.project_executors).join(ProjectExecutors.user_info)
    if join_status:
        stmt = stmt.join(Projects.project_info)

    stmt = stmt.options(
        selectinload(Projects.object_info),
        selectinload(Projects.contract_info),
        selectinload(Projects.executor_info),
        selectinload(Projects.project_info),
        selectinload(Projects.project_executors).selectinload(
            ProjectExecutors.user_info
        ),
        selectinload(Projects.project_executors).selectinload(
            ProjectExecutors.project_info
        ),
        selectinload(Projects.contract_info).selectinload(Contracts.customer_info),
    )

    filters = []

    if id:
        filters.append(Projects.id.in_(id))
    if number:
        filters.append(or_(Projects.number.ilike(f"%{num}%") for num in number))

    if object:
        if not join_object:
            stmt = stmt.join(Projects.object_info)
        filters.append(or_(Objects.code.ilike(f"%{code}%") for code in object))

    if name:
        if not join_object:
            stmt = stmt.join(Projects.object_info)
        filters.append(or_(Objects.name.ilike(f"%{name}%") for name in name))

    if contract:
        if not join_contract:
            stmt = stmt.join(Projects.contract_info)
        filters.append(or_(Contracts.number.ilike(f"%{num}%") for num in contract))

    if main_executor:
        if not join_main_executor:
            stmt = stmt.join(Projects.executor_info)
        filters.append(
            or_(
                or_(
                    Users.full_name.ilike(f"%{name}%"),
                    Users.first_name.ilike(f"%{name}%"),
                    Users.last_name.ilike(f"%{name}%"),
                )
                for name in main_executor
            )
        )

    if project_executor:
        if not join_project_executor:
            stmt = stmt.join(Projects.project_executors).join(
                ProjectExecutors.user_info
            )
        filters.append(
            or_(
                or_(
                    Users.full_name.ilike(f"%{name}%"),
                    Users.first_name.ilike(f"%{name}%"),
                    Users.last_name.ilike(f"%{name}%"),
                )
                for name in project_executor
            )
        )

    if deadline:
        filters.append(Projects.deadline.in_(deadline))

    if status:
        if not join_status:
            stmt = stmt.join(Projects.project_info)
        filters.append(or_(ProjectStatuses.name.ilike(f"%{name}%") for name in status))

    if notes:
        filters.append(or_(Projects.notes.ilike(f"%{note}%") for note in notes))

    if filters:
        stmt = stmt.where(and_(*filters))

    if sortBy:
        if sortBy == "object":
            if not join_object:
                stmt = stmt.join(Projects.object_info)
            sort_column = Objects.code
        elif sortBy == "name":
            if not join_object:
                stmt = stmt.join(Projects.object_info)
            sort_column = Objects.name
        elif sortBy == "number":
            if not join_contract:
                stmt = stmt.join(Projects.contract_info)
            sort_column = Contracts.number
        elif sortBy == "main_executor":
            if not join_main_executor:
                stmt = stmt.join(Projects.executor_info)
            sort_column = Users.full_name
        elif sortBy == "project_executor":
            if not join_project_executor:
                stmt = stmt.join(Projects.project_executors).join(
                    ProjectExecutors.user_info
                )
            sort_column = Users.full_name
        elif sortBy == "status":
            if not join_status:
                stmt = stmt.join(Projects.project_info)
            sort_column = ProjectStatuses.name
        else:
            try:
                sort_column = getattr(Projects, sortBy)
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
    projects = result.scalars().all()

    response = []
    for project in projects:
        response.append(
            {
                "id": project.id,
                "object": (
                    {
                        "id": project.object_info.id,
                        "code": project.object_info.code,
                        "name": project.object_info.name,
                        "comment": project.object_info.comment,
                    }
                    if project.object_info
                    else None
                ),
                "contract": (
                    {
                        "id": project.contract_info.id,
                        "code": project.contract_info.code,
                        "name": project.contract_info.name,
                        "customer": project.contract_info.customer_info,
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
                "main_executor": (
                    {
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
                    }
                    if project.executor_info
                    else None
                ),
                "deadline": project.deadline,
                "status": (
                    {
                        "id": project.project_info.id,
                        "name": project.project_info.name,
                    }
                    if project.project_info
                    else None
                ),
                "notes": project.notes,
                "project_executors": [
                    {
                        "id": executor.id,
                        "user": {
                            **executor.user_info.__dict__,
                            "password": None,
                        },
                    }
                    for executor in project.project_executors
                ],
            }
        )
    return response


@router.get("/projects/{project_id}")
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
            selectinload(Projects.contract_info).selectinload(Contracts.customer_info),
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
                "customer": project.contract_info.customer_info,
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
    # Проверка на уникальность поля number
    result = await db.execute(
        select(Projects).filter(Projects.number == project_data.number)
    )
    existing_project = result.scalar_one_or_none()
    if existing_project:
        raise HTTPException(
            status_code=400, detail="Проект с таким номером уже существует"
        )

    project = Projects(**project_data.dict())
    db.add(project)
    try:
        await db.commit()
    except exc.IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail="Проект с таким номером уже существует"
        )
    await db.refresh(project)
    return project


@router.patch("/projects/{project_id}", response_model=ProjectGetResponse)
@log_action("Обновление проекта")
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
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

    # Проверка на уникальность поля number
    if project_data.number:
        result = await db.execute(
            select(Projects).filter(
                Projects.number == project_data.number, Projects.id != project_id
            )
        )
        existing_project = result.scalar_one_or_none()
        if existing_project:
            raise HTTPException(
                status_code=400, detail="Проект с таким номером уже существует"
            )

    for key, value in project_data.dict(exclude_unset=True).items():
        setattr(project, key, value)

    try:
        await db.commit()
    except exc.IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail="Проект с таким номером уже существует"
        )
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
