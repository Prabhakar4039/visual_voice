"""
utils/logger.py — Structured logging setup for the application.

Call setup_logging() once at app start. All other modules get their
logger via logging.getLogger(__name__).
"""

from __future__ import annotations

import logging
import logging.handlers
import os
from pathlib import Path


def setup_logging(log_dir: Path | None = None) -> None:
    """
    Configure root logger with both console and rotating file handlers.

    Args:
        log_dir: Directory for log files. Defaults to ./logs relative to CWD.
    """
    if log_dir is None:
        log_dir = Path(os.getcwd()) / "logs"

    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "app.log"

    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    date_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt=date_fmt)

    # Rotating file handler — max 5 MB, 3 backups
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Avoid adding duplicate handlers on Streamlit reruns
    if not root_logger.handlers:
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

    # Quieten noisy third-party loggers
    for noisy in ("transformers", "torch", "httpx", "httpcore", "openai"):
        logging.getLogger(noisy).setLevel(logging.WARNING)
