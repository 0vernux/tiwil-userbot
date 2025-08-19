# core/logger_mod.py

import logging
import os
from pathlib import Path

Path("logs").mkdir(exist_ok=True)

log_path = Path("logs/bot.log")
log_path.touch(exist_ok=True)  # создаст пустой файл, если его нет

logger = logging.getLogger("bot_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs/bot.log", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

if not logger.handlers:
    logger.addHandler(file_handler)