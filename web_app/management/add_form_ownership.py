from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from web_app.database import get_db
from fastapi import HTTPException, APIRouter, Depends, status
from web_app.models.form_of_ownerships import FormOfOwnerships


async def add_initial_forms_of_ownership(db: AsyncSession = Depends(get_db)):
    forms = ["ООО", "ЗАО", "ИП"]

    stmt = select(FormOfOwnerships)
    result = await db.execute(stmt)
    form_of_ownerships = result.scalars().all()

    existing_forms = {form.name for form in form_of_ownerships}

    for form_name in forms:
        if form_name not in existing_forms:
            db.add(FormOfOwnerships(name=form_name))

    await db.commit()
