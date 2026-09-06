# image/generator.py

import os
import requests
from config.settings import settings
from utils.logger import logger
from utils.helpers import get_random_local_image
from datetime import datetime


SEARCH_QUERIES = {
    "تعليمي": "herbal tea natural health mushroom",
    "شخصي":   "morning tea cozy home lifestyle",
    "نصيحة":  "healthy lifestyle wellness routine",
    "تفاعلي": "coffee tea drinks comparison",
    "منتج":   "natural tea herbs organic",
    "سؤال_شائع": "tea cup steam natural herbs",
    "محفز":   "morning motivation healthy life nature"
}


def generate_image_from_api(post_type: str, post_text: str) -> str | None:
    """
    بتجيب صورة من Unsplash مجاناً
    حسب نوع البوست
    """
    if not settings.IMAGE_API_KEY:
        logger.warning("⚠️ No Image API Key found")
        return None

    try:
        logger.info(f"🎨 Getting image from Unsplash for: {post_type}")

        query = SEARCH_QUERIES.get(post_type, "healthy tea natural")

        # بنجيب صورة عشوائية من Unsplash
        response = requests.get(
            "https://api.unsplash.com/photos/random",
            params={
                "query": query,
                "orientation": "squarish",
                "content_filter": "high"
            },
            headers={
                "Authorization": f"Client-ID {settings.IMAGE_API_KEY}"
            },
            timeout=15
        )

        if response.status_code != 200:
            logger.error(f"❌ Unsplash error: {response.text}")
            return None

        data = response.json()
        image_url = data["urls"]["regular"]

        # بنحمل الصورة
        img_response = requests.get(image_url, timeout=30)

        if img_response.status_code != 200:
            logger.error("❌ Failed to download image")
            return None

        # بنحفظ الصورة
        os.makedirs("image/generated", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = f"image/generated/{post_type}_{timestamp}.jpg"

        with open(image_path, "wb") as f:
            f.write(img_response.content)

        logger.info(f"✅ Image saved: {image_path}")
        return image_path

    except requests.Timeout:
        logger.error("❌ Timeout getting image from Unsplash")
        return None

    except Exception as e:
        logger.error(f"❌ Unsplash error: {e}")
        return None


def get_post_image(post_type: str, post_text: str) -> str | None:
    """
    الدالة الرئيسية لجلب صورة البوست
    بتجرب Unsplash الأول
    لو فشل بتاخد صورة محلية
    لو مفيش بترجع None
    """

    # أولاً: Unsplash
    image_path = generate_image_from_api(post_type, post_text)

    if image_path:
        return image_path

    # تانياً: صور محلية
    logger.info(f"📁 Trying local images for: {post_type}")
    local_image = get_random_local_image(post_type)

    if local_image:
        logger.info(f"✅ Using local image: {local_image}")
        return local_image

    # تالتاً: بدون صورة
    logger.warning(f"⚠️ No image found, posting without image")
    return None