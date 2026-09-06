# main.py

from config.settings import settings
from content.generator import setup_gemini
from publisher.facebook import verify_page_access
from scheduler.job import run_daily_job
from utils.helpers import create_local_image_folders
from utils.logger import logger
import sys


def initialize():
    logger.info("🔧 Initializing DXN Social Media Bot...")

    if not settings.validate():
        logger.error("❌ Invalid settings, exiting...")
        sys.exit(1)

    setup_gemini()

    if not verify_page_access():
        logger.error("❌ Facebook page access failed, exiting...")
        sys.exit(1)

    create_local_image_folders()
    logger.info("✅ Initialization complete!")


if __name__ == "__main__":
    initialize()
    run_daily_job()