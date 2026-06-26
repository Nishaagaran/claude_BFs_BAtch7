"""Centralized logging configuration for Patient Health Analyzer.

Provides a single configuration point for all logging setup and management.
"""

import logging
import sys
from typing import Optional


def setup_logger(
    name: str,
    log_file: str,
    level: int = logging.INFO,
    console_level: Optional[int] = None,
) -> logging.Logger:
    """Configure and return a logger instance.

    Sets up both file and console handlers with consistent formatting.

    Args:
        name (str): Name of the logger (typically __name__)
        log_file (str): Path to the log file
        level (int): Logging level for file handler (default: logging.INFO)
        console_level (Optional[int]): Logging level for console handler
                                       (default: same as level)

    Returns:
        logging.Logger: Configured logger instance
    """
    if console_level is None:
        console_level = level

    logger = logging.getLogger(name)
    logger.setLevel(min(level, console_level))

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get an existing logger by name.

    Args:
        name (str): Name of the logger

    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)
