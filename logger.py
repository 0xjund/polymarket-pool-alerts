import logging
from datetime import datetime
import os

def setup_logger(name = 'polymarket_bot', log_file = 'bot.log', level=logging.INFO):
    """
    Setup logging

    Args:
        name: Logger name
        log_file: Path to log file
        level: Logging level(DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """

    # Create log dir if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers if setup_logger is called multiple times
    if logger.handlers:
        return logger 

    # Create formatter
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # Add handlers to logger 
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger 
