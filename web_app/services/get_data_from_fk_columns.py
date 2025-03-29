from sqlalchemy import select, distinct

from web_app.models import (
    Contracts,
    Customers,
    Users,
    Objects,
    ProjectStatuses,
    FormOfOwnerships,
)

RELATION_MAPPING = {
    "agreements.contract": ("Contracts", "name"),
    "customers.form": ("FormOfOwnerships", "name"),
    "contacts.customer": ("Customers", "name"),
    "contracts.code": ("Objects", "code"),
    "contracts.executor": ("Users", "full_name"),
    "contracts.customer": ("Customers", "name"),
    "projects.object": ("Objects", "code"),
    "projects.contract": ("Contracts", "number"),
    "projects.main_executor": ("Users", "full_name"),
    "projects.status": ("ProjectStatuses", "name"),
}

MODEL_MAPPING = {
    "Contracts": Contracts,
    "Customers": Customers,
    "Users": Users,
    "Objects": Objects,
    "ProjectStatuses": ProjectStatuses,
    "FormOfOwnerships": FormOfOwnerships,
}


def get_relation_info(table, column_name):
    key = f"{table.__tablename__}.{column_name}"
    return RELATION_MAPPING.get(key)


async def get_unique_values(db, table, column_name):
    try:
        column_attr = getattr(table, column_name)
        relation_info = get_relation_info(table, column_name)
        print(relation_info)

        if relation_info:
            related_model_name, display_field = relation_info
            related_model = MODEL_MAPPING.get(related_model_name)

            if not related_model:
                raise ValueError(f"Model {related_model_name} not found")

            display_attr = getattr(related_model, display_field)

            stmt = (
                select(distinct(display_attr))
                .select_from(table)
                .join(related_model, column_attr == related_model.id)
                .where(display_attr.isnot(None))
                .order_by(display_attr)
            )
        else:
            stmt = (
                select(distinct(column_attr))
                .where(column_attr.isnot(None))
                .order_by(column_attr)
            )

        result = await db.execute(stmt)
        return result.scalars().all()

    except Exception as e:
        print(f"Error getting values for {table.__name__}.{column_name}: {str(e)}")
        return []
