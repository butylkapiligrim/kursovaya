import logging


def loggingg() -> logging.Logger:
    """
    Функция, которая настраивает логирование.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(module)s - %(levelname)s - %(message)s",
        encoding="utf-8",
        handlers=[logging.FileHandler("logs_file.log", mode="w")],
    )
    return logging.getLogger(__name__)
