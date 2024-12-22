import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Directories
BASE_DIR = Path("web_app/static")
UPLOAD_DIRECTORY = BASE_DIR / "uploads"
LOGO_DIRECTORY = BASE_DIR / "img"

# Ensure directories exist
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
LOGO_DIRECTORY.mkdir(parents=True, exist_ok=True)
logger.info(f"Directories ensured: {UPLOAD_DIRECTORY}, {LOGO_DIRECTORY}")


async def get_most_recent_file(directory: Path) -> str | None:
    """Get the most recently created file in the given directory."""
    try:
        files = list(directory.iterdir())
        if files:
            most_recent_file = max(files, key=lambda f: f.stat().st_ctime)
            logger.info(f"Most recent file in {directory}: {most_recent_file.name}")
            return most_recent_file.name
        else:
            logger.warning(f"No files found in directory: {directory}")
    except FileNotFoundError as e:
        logger.error(f"Directory not found: {directory}. Error: {e}")
    return None


async def get_logo() -> str | None:
    """Get the most recent logo file."""
    logger.info("Fetching the most recent logo file...")
    return await get_most_recent_file(LOGO_DIRECTORY)


async def get_bg() -> str | None:
    """Get the most recent background file."""
    logger.info("Fetching the most recent background file...")
    return await get_most_recent_file(UPLOAD_DIRECTORY)
