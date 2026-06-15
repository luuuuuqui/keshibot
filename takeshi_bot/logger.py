from __future__ import annotations

import logging

from .paths import TEMP_DIR

LOG_FILE = TEMP_DIR / "wa-logs-python.txt"


def configure_logging() -> None:
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
        ],
    )


def banner_log() -> None:
    logging.info("Takeshi Bot Python")


def info_log(message: str) -> None:
    logging.info(message)


def success_log(message: str) -> None:
    logging.info(message)


def warning_log(message: str) -> None:
    logging.warning(message)


def error_log(message: str, error: object | None = None) -> None:
    if error is None:
        logging.error(message)
    else:
        logging.error("%s %s", message, error)


def input_log(message: str) -> None:
    logging.info(message)


def say_log(message: str) -> None:
    logging.info(message)
