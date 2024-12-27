import logging
from fastapi import APIRouter, File, UploadFile, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Настройка статических файлов и шаблонов
router.mount("/static", StaticFiles(directory="web_app/static"), name="static")

# Путь для сохранения загруженных изображений
UPLOAD_DIRECTORY = "web_app/static/uploads"
LOGO_DIRECTORY = "web_app/static/img"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@router.get("/customaze", response_class=JSONResponse)
async def read_root(request: Request):
    logger.info("Accessing customization page")
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

    return {
        "request": str(request.url),
        "bg_filename": bg_file,
        "logo_file": logo_file,
    }


@router.post("/upload_image/")
async def upload_image(file: UploadFile = File(...)):
    logger.info(f"Uploading image: {file.filename}")
    file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    logger.info(f"Image uploaded successfully: {file.filename}")
    return JSONResponse(
        content={"message": "Image uploaded successfully"},
        status_code=status.HTTP_200_OK,
    )


@router.post("/upload-logo/")
async def upload_logo(file: UploadFile = File(...)):
    logger.info(f"Uploading logo: {file.filename}")
    file_location = f"{LOGO_DIRECTORY}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    logger.info(f"Logo uploaded successfully: {file.filename}")
    return JSONResponse(
        content={"message": "Logo uploaded successfully"},
        status_code=status.HTTP_200_OK,
    )
