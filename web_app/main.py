from fastapi import FastAPI

from web_app.management.add_form_ownership import add_initial_forms_of_ownership
from web_app.routes import (
    custom,
    auth,
    users,
    objects,
    agreements,
    form_of_ownerships,
    customers,
)
from web_app.database import init_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await add_initial_forms_of_ownership()
    yield


app = FastAPI(lifespan=lifespan)

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent / "static"),
    name="static",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(custom.router)
app.include_router(objects.router)
app.include_router(agreements.router)
app.include_router(form_of_ownerships.router)
app.include_router(customers.router)

origins = [
    "http://localhost:3000",  # React production server
    "http://localhost:5173",  # React development server
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
