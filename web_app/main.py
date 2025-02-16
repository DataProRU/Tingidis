from fastapi import FastAPI

from web_app.management.add_form_ownership import add_initial_forms_of_ownership
from web_app.management.add_project_status import add_initial_project_statuses
from web_app.routes import (
    custom,
    auth,
    users,
    objects,
    agreements,
    form_of_ownerships,
    customers,
    contacts,
    logs,
    contracts,
    backup,
    project_statuses,
    projects,
    project_executors,
)
from web_app.database import init_db, async_session
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    async with async_session() as db:
        await add_initial_forms_of_ownership(db)
        await add_initial_project_statuses(db)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(custom.router)
app.include_router(objects.router)
app.include_router(agreements.router)
app.include_router(form_of_ownerships.router)
app.include_router(customers.router)
app.include_router(contacts.router)
app.include_router(contracts.router)
app.include_router(logs.router)
app.include_router(project_statuses.router)
app.include_router(projects.router)
app.include_router(project_executors.router)
app.include_router(backup.router)

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
