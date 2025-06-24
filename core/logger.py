from loguru import logger
import sys
import os

# Remove default logger
logger.remove()

if not os.path.exists("logs"):
    os.makedirs("logs")

logger.add(
    "logs/app.log",
    rotation="1 week",
    retention="1 month",
    level="INFO",
    encoding="utf8",
    enqueue=True,
    backtrace=True,
    diagnose=True,
)

# Add logging to stderr (console)
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>",
    level="INFO",
    backtrace=True,
    diagnose=True,
)
