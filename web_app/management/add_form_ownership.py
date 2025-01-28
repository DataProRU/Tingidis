from sqlalchemy.ext.asyncio import AsyncSession
from web_app.models.form_of_ownerships import FormOfOwnerships
from web_app.database import get_db


async def add_initial_forms_of_ownership():
    forms = ["ООО", "ЗАО", "ИП"]

    # Используем async with для получения сессии
    async for db in get_db():
        for form_name in forms:
            db_form = FormOfOwnerships(name=form_name)
            db.add(db_form)
        await db.commit()
        await db.close()
