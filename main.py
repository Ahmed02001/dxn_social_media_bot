# main.py

from config.settings import settings
from content.generator import setup_gemini
from publisher.facebook import verify_page_access
from scheduler.job import start_scheduler, run_daily_job
from utils.helpers import create_local_image_folders
from utils.logger import logger
import sys


def initialize():
    """
    بنعمل كل الـ setup الأول
    قبل ما نبدأ أي حاجة
    """
    
    logger.info("🔧 Initializing DXN Social Media Bot...")
    
    # الخطوة 1: بنتأكد من الـ API Keys
    if not settings.validate():
        logger.error("❌ Invalid settings, exiting...")
        sys.exit(1)
    
    # الخطوة 2: بنعمل setup للـ Gemini
    setup_gemini()
    
    # الخطوة 3: بنتأكد من صلاحية الفيسبوك
    if not verify_page_access():
        logger.error("❌ Facebook page access failed, exiting...")
        sys.exit(1)
    
    # الخطوة 4: بنعمل فولدرات الصور المحلية
    create_local_image_folders()
    
    logger.info("✅ Initialization complete!")


if __name__ == "__main__":
    
    # بنعمل initialize الأول
    initialize()
    
    # لو عايز تجرب بوست واحد دلوقتي
    # من غير scheduler
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        logger.info("🧪 Running in test mode...")
        from scheduler.job import run_daily_job
        run_daily_job()
    else:
        # بنشغل الـ scheduler الأوتوماتيك
        logger.info("🤖 Starting automated scheduler...")
        start_scheduler() 