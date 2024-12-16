from fastapi import FastAPI, File, UploadFile, Request, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os

router = APIRouter()

# Настройка статических файлов и шаблонов
router.mount("/static", StaticFiles(directory="web_app/static"), name="static")
templates = Jinja2Templates(directory="web_app/templates")

# Путь для сохранения загруженных изображений
UPLOAD_DIRECTORY = "web_app/static/uploads"
LOGO_DIRECTORY = "web_app/static/img"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@router.get("/customaze", response_class=HTMLResponse)
async def read_root(request: Request):
    # Получаем последнее загруженное изображение

    logo_files = os.listdir(LOGO_DIRECTORY)
    bg_files = os.listdir(UPLOAD_DIRECTORY)
    if logo_files and bg_files:
        logo_file = max(
            logo_files, key=lambda f: os.path.getctime(os.path.join(LOGO_DIRECTORY, f))
        )
        bg_file = max(
            bg_files, key=lambda f: os.path.getctime(os.path.join(UPLOAD_DIRECTORY, f))
        )
    else:
        logo_file = None
        bg_file = None
    return templates.TemplateResponse(
        "custom.html",
        {"request": request, "bg_filename": bg_file, "logo_file": logo_file},
    )


@router.post("/upload_image/")
async def upload_image(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return RedirectResponse(url="/customaze", status_code=303)


@router.post("/upload-logo/")
async def upload_logo(file: UploadFile = File(...)):
    file_location = f"{LOGO_DIRECTORY}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return RedirectResponse(url="/customaze", status_code=303)
