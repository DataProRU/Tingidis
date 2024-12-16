from fastapi import FastAPI
from web_app.routes import custom, auth_routes, users
from web_app.database import init_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте приложения создаем таблицы
    await init_db()
    yield  # This is where the app runs
    # Optionally, you can add any shutdown logic here if needed


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="web_app/static"), name="static")
app.include_router(auth_routes.router)
app.include_router(users.router)
app.include_router(custom.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
