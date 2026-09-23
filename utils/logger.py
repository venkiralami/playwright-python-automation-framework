import logging
from pathlib import Path

LOG_DIR = Path("reports/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

def get_logger(name):

    logger = logging.getLogger(name)

    if not logger.handlers:

        logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

        file_handler = logging.FileHandler(LOG_DIR / "automation.log", encoding="utf-8")

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger