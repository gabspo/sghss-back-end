"""Logging configuration for SGHSS application."""

import logging
import logging.handlers
import os
from datetime import datetime


def setup_logging(log_level: str = "INFO", log_dir: str = "logs") -> None:
    """
    Configure logging for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_dir: Directory to store log files.
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler with rotation
    log_filename = os.path.join(log_dir, f"sghss-{datetime.now().date()}.log")
    file_handler = logging.handlers.RotatingFileHandler(
        log_filename,
        maxBytes=10485760,  # 10MB
        backupCount=10,
    )
    file_handler.setLevel(getattr(logging, log_level))
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Log initial message
    root_logger.info("Logging configured successfully")
