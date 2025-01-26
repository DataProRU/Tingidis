from fastapi import HTTPException, APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from web_app.database import get_db
from sqlalchemy.future import select
from web_app.models.customers import Customers
from web_app.schemas.customers import CustomerCreate, CustomerUpdate, CustomerResponse
from web_app.middlewares.auth_middleware import token_verification_dependency

router = APIRouter()


# Endpoints
@router.get("/customers", response_model=List[CustomerResponse])
async def get_customers(
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    stmt = select(Customers)
    result = await db.execute(stmt)
    customers = result.scalars().all()
    return customers


@router.get("/customers/{customer_id}", response_model=CustomerResponse)
async def get_customer_by_id(
    customer_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(select(Customers).filter(Customers.id == customer_id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return customer


@router.post(
    "/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED
)
async def create_customer(
    customer_data: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    customer = Customers(**customer_data.dict())
    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    return customer


@router.patch("/customers/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: int,
    customer_data: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    result = await db.execute(select(Customers).filter(Customers.id == customer_id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Клиент не найден")

    for key, value in customer_data.dict(exclude_unset=True).items():
        setattr(customer, key, value)

    await db.commit()
    await db.refresh(customer)
    return customer


@router.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    customer_id: int,
    db: AsyncSession = Depends(get_db),
    user_data: dict = Depends(token_verification_dependency),
):
    # Проверка наличия объекта
    result = await db.execute(select(Customers).filter(Customers.id == customer_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Клиент не найден")

    # Удаление объекта
    await db.delete(obj)
    await db.commit()
    return {"message": "Клиент успешно удален", "customer_id": customer_id}
