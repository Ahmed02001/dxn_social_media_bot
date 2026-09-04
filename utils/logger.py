import logging
import os
from datetime import datetime

def setup_logger() -> logging.Logger:
    """
    بنعمل logger بيسجل كل حاجة
    في الـ console وفي ملف log
    """
    
    # بنعمل فولدر logs لو مش موجود
    os.makedirs("logs", exist_ok=True)
    
    # اسم الـ logger
    logger = logging.getLogger("DXNBot")
    logger.setLevel(logging.DEBUG)
    
    # Format بتاع الـ log
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Handler للـ console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Handler للـ file
    file_handler = logging.FileHandler(
        f"logs/bot.log",
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # بنضيف الـ handlers للـ logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# بنعمل instance واحد بس
logger = setup_logger()