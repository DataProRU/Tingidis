"""from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

def add_initial_forms_of_ownership():
    db = SessionLocal()
    forms = ["ООО", "ЗАО", "ИП"]
    for form_name in forms:
        db_form = models.FormOfOwnership(name=form_name)
        db.add(db_form)
    db.commit()
    db.close()

if __name__ == "__main__":
    add_initial_forms_of_ownership()"""
