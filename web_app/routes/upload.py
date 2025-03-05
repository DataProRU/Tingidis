import os

from fastapi import File, UploadFile, APIRouter

router = APIRouter()


@router.post("/upload-bg")
async def upload_file(file: UploadFile = File(...)):
    from web_app.main import UPLOAD_DIR

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    new_file_name = f"bg.{file_extension}"
    file_location = os.path.join(UPLOAD_DIR, new_file_name)

    with open(file_location, "wb+") as file_object:
        file_object.write(await file.read())

    return {"url": f"/static/{new_file_name}"}


@router.post("/upload-logo")
async def upload_logo(file: UploadFile = File(...)):
    from web_app.main import UPLOAD_DIR

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_extension = file.filename.split(".")[-1] if "." in file.filename else "png"
    new_file_name = f"logo.{file_extension}"
    file_location = os.path.join(UPLOAD_DIR, new_file_name)

    with open(file_location, "wb+") as file_object:
        file_object.write(await file.read())

    return {"url": f"/static/{new_file_name}"}
