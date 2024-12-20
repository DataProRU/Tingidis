import os

UPLOAD_DIRECTORY = "web_app/static/uploads"
LOGO_DIRECTORY = "web_app/static/img"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


def get_logo():
    logo_files = os.listdir(LOGO_DIRECTORY)
    if logo_files:
        logo_file = max(
            logo_files, key=lambda f: os.path.getctime(os.path.join(LOGO_DIRECTORY, f))
        )
    else:
        logo_file = None
    return logo_file


def get_bg():
    bg_files = os.listdir(UPLOAD_DIRECTORY)
    if bg_files:
        bg_file = max(
            bg_files, key=lambda f: os.path.getctime(os.path.join(UPLOAD_DIRECTORY, f))
        )
    else:
        bg_file = None
    return bg_file
