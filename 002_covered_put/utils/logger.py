import logging
import sys
from utils.config import LOG_PATH

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(LOG_PATH)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

strat_logger = get_logger("CoveredPutPro")