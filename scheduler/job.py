# scheduler/job.py

import schedule
import time
from config.content_schedule import get_today_post_type
from config.settings import settings
from content.generator import generate_post
from image.generator import get_post_image
from publisher.facebook import publish
from utils.logger import logger


def run_daily_job():
    """
    الجوب اليومي الرئيسي
    بيشغل كل الخطوات من توليد المحتوى للنشر
    """
    
    logger.info("=" * 50)
    logger.info("🚀 Starting daily post job...")
    logger.info("=" * 50)
    
    try:
        # الخطوة 1: نحدد نوع البوست لليوم ده
        post_type = get_today_post_type()
        logger.info(f"📅 Post type for today: {post_type}")
        
        # الخطوة 2: نولد نص البوست
        logger.info("📝 Generating post content...")
        post_text = generate_post(post_type)
        
        # الخطوة 3: نجيب صورة مناسبة
        logger.info("🖼️ Getting post image...")
        image_path = get_post_image(post_type, post_text)
        
        # الخطوة 4: ننشر على فيسبوك
        logger.info("📤 Publishing to Facebook...")
        result = publish(post_text, image_path)
        
        logger.info("=" * 50)
        logger.info(f"✅ Daily job completed successfully!")
        logger.info(f"📊 Post ID: {result.get('id', 'Unknown')}")
        logger.info("=" * 50)
        
    except Exception as e:
        logger.error("=" * 50)
        logger.error(f"❌ Daily job failed: {e}")
        logger.error("=" * 50)


def start_scheduler():
    """
    بيبدأ الـ scheduler ويشغله
    هينشر كل يوم في الوقت المحدد في الـ .env
    """
    
    post_time = settings.POST_TIME
    
    logger.info(f"⏰ Scheduler started, will post daily at {post_time}")
    
    # بنجدول الجوب اليومي
    schedule.every().day.at(post_time).do(run_daily_job)
    
    # بنشغل الجوب فوراً للتجربة لو حابب
    # run_daily_job()
    
    # Loop اللي بيشغل الـ scheduler
    while True:
        schedule.run_pending()
        time.sleep(60)