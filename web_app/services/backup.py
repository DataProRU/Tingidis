import logging
import subprocess

logger = logging.getLogger(__name__)


def create_database_dump(
    container_name: str, db_user: str, db_name: str, dump_path: str
) -> str:
    try:
        create_dump_command = [
            "docker",
            "exec",
            container_name,
            "pg_dump",
            "-U",
            db_user,
            "-d",
            db_name,
            "-f",
            dump_path,
        ]
        subprocess.run(create_dump_command, check=True)
        logger.info(f"Дамп базы данных создан: {dump_path}")
        return dump_path
    except subprocess.CalledProcessError as e:
        logger.error(f"Ошибка при создании дампа: {e}")
        raise


def copy_dump_from_container(
    container_name: str, container_dump_path: str, local_dump_path: str
) -> str:
    try:
        copy_dump_command = [
            "docker",
            "cp",
            f"{container_name}:{container_dump_path}",
            local_dump_path,
        ]
        subprocess.run(copy_dump_command, check=True)
        logger.info(f"Дамп скопирован на локальную машину: {local_dump_path}")
        return local_dump_path
    except subprocess.CalledProcessError as e:
        logger.error(f"Ошибка при копировании дампа: {e}")
        raise
