
import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger():
    """Set up logging for Sakhi."""

    # Create the logs folder if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("SAKHI")
    logger.setLevel(logging.DEBUG)

    # Don't add the same handler more than once
    if logger.handlers:
        return logger

    # Choose how each log message looks
    log_format = "%(asctime)s | %(levelname)s | %(message)s"
    formatter = logging.Formatter(log_format)

    # Save logs to a file, keeping up to three backups
    file_handler = RotatingFileHandler(
        "logs/sakhi.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger

