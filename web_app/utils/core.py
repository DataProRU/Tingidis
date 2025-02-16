from sqlalchemy.orm import class_mapper


def model_to_dict(model):
    return {
        column.name: getattr(model, column.name)
        for column in class_mapper(model.__class__).mapped_table.c
    }
