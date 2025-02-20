from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

@app.post("/reserve-copy/")
def create_reserve_copy(reserve_copy: ReserveCopyCreate):
    db = SessionLocal()

    # Calculate send_date based on frequency
    today = datetime.now().date()
    if reserve_copy.frequency == 1:
        send_date = today + timedelta(days=7)
    elif reserve_copy.frequency == 2:
        send_date = today + timedelta(days=30)
    elif reserve_copy.frequency == 3:
        send_date = today + timedelta(days=90)
    elif reserve_copy.frequency == 4:
        send_date = today + timedelta(days=180)
    elif reserve_copy.frequency == 5:
        send_date = today + timedelta(days=365)

    db_reserve_copy = ReserveCopy(email=reserve_copy.email, frequency=reserve_copy.frequency, send_date=send_date)
    db.add(db_reserve_copy)
    db.commit()
    db.refresh(db_reserve_copy)

    return db_reserve_copy