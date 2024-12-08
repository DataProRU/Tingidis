from fastapi import FastAPI
from routes import users, auth_routes
from database import init_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth_routes.router)
app.include_router(users.router)


@app.on_event("startup")
async def startup():
    # При старте приложения создаем таблицы
    await init_db()


@app.on_event("shutdown")
async def shutdown():
    # Отключаемся от базы данных при завершении работы
    await database.disconnect()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
