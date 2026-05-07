import logging
import os


def get_logger(name: str = "pipeline") -> logging.Logger:
    """
    Returns a configured logger instance.
    """

    logger = logging.getLogger(name)

    # Evita duplicar handlers si ya existe
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # Crear carpeta logs si no existe
    os.makedirs("logs", exist_ok=True)

    log_file_path = os.path.join("logs", "pipeline.log")

    # Formato estándar
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Handler para archivo
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Agregar handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger