import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logger(name: str = "ProtectiveCall", log_file: str = "strategy.log"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG) 

    if logger.hasHandlers():
        return logger

    console_format = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt='%H:%M:%S')
    file_format = logging.Formatter('%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s')

    c_handler = logging.StreamHandler(sys.stdout)
    c_handler.setLevel(logging.INFO)
    c_handler.setFormatter(console_format)

    log_path = Path("logs")
    log_path.mkdir(exist_ok=True)
    
    f_handler = RotatingFileHandler(
        log_path / log_file, 
        maxBytes=5*1024*1024, 
        backupCount=3 
    )
    f_handler.setLevel(logging.DEBUG)
    f_handler.setFormatter(file_format)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger