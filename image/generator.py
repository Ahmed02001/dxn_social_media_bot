# image/generator.py

import os
import requests
from config.settings import settings
from utils.logger import logger
from utils.helpers import get_random_local_image


def generate_image_from_api(post_type: str, post_text: str) -> str | None:
    """
    بتولد صورة من الـ API
    دلوقتي بنستخدم Stability AI
    لو مش عندك API Key هترجع None
    
    Args:
        post_type: نوع البوست
        post_text: نص البوست عشان نعمل prompt مناسب
    
    Returns:
        str | None: مسار الصورة المولدة أو None
    """
    
    # لو مفيش API Key نرجع None
    if not settings.IMAGE_API_KEY:
        logger.warning("⚠️ No Image API Key found, skipping API generation")
        return None
    
    try:
        logger.info(f"🎨 Generating image from API for type: {post_type}")
        
        # بنعمل prompt للصورة حسب نوع البوست
        image_prompt = get_image_prompt(post_type)
        
        # Stability AI API
        url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        
        headers = {
            "Authorization": f"Bearer {settings.IMAGE_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        body = {
            "text_prompts": [
                {
                    "text": image_prompt,
                    "weight": 1
                },
                {
                    # Negative prompt عشان نتجنب حاجات معينة
                    "text": "blurry, low quality, text, watermark, logo",
                    "weight": -1
                }
            ],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        }
        
        response = requests.post(url, headers=headers, json=body)
        
        if response.status_code != 200:
            logger.error(f"❌ Image API error: {response.text}")
            return None
        
        # بنحفظ الصورة
        data = response.json()
        image_data = data["artifacts"][0]["base64"]
        
        # بنعمل فولدر للصور المولدة
        os.makedirs("image/generated", exist_ok=True)
        
        import base64
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = f"image/generated/{post_type}_{timestamp}.png"
        
        with open(image_path, "wb") as f:
            f.write(base64.b64decode(image_data))
        
        logger.info(f"✅ Image generated and saved: {image_path}")
        return image_path
        
    except requests.RequestException as e:
        logger.error(f"❌ Request error in generate_image_from_api: {e}")
        return None
        
    except Exception as e:
        logger.error(f"❌ Unexpected error in generate_image_from_api: {e}")
        return None


def get_image_prompt(post_type: str) -> str:
    """
    بترجع الـ prompt المناسب لكل نوع بوست
    عشان الصورة تكون مناسبة للمحتوى
    
    Args:
        post_type: نوع البوست
    
    Returns:
        str: prompt الصورة
    """
    
    # إعدادات ثابتة لكل الصور
    base_style = (
        "professional photography, warm lighting, "
        "natural colors, high quality, realistic"
    )
    
    prompts = {
        "تعليمي": (
            f"A cup of herbal tea with green leaves and mushrooms "
            f"on a wooden table, educational feel, {base_style}"
        ),
        "شخصي": (
            f"A person holding a warm cup of tea in the morning, "
            f"cozy home atmosphere, soft natural light, {base_style}"
        ),
        "نصيحة": (
            f"Healthy lifestyle flat lay with tea cup, fresh fruits, "
            f"and green plants on white background, {base_style}"
        ),
        "تفاعلي": (
            f"Two cups of different drinks side by side, "
            f"coffee vs tea comparison, clean background, {base_style}"
        ),
        "منتج": (
            f"DXN tea product packaging with natural herbs and mushrooms "
            f"on elegant dark background, product photography, {base_style}"
        ),
        "سؤال_شائع": (
            f"Close up of herbal tea being poured into a glass cup, "
            f"steam rising, natural herbs visible, {base_style}"
        ),
        "محفز": (
            f"Morning sunrise with a person enjoying tea outdoors, "
            f"peaceful and motivational atmosphere, {base_style}"
        )
    }
    
    return prompts.get(post_type, prompts["تعليمي"])


def get_post_image(post_type: str, post_text: str) -> str | None:
    """
    الدالة الرئيسية لجلب صورة البوست
    بتجرب API الأول، لو فشل بتاخد صورة محلية
    لو مفيش صور محلية بترجع None وينشر بدون صورة
    
    Args:
        post_type: نوع البوست
        post_text: نص البوست
    
    Returns:
        str | None: مسار الصورة أو None
    """
    
    # أولاً: نجرب نولد من API
    image_path = generate_image_from_api(post_type, post_text)
    
    if image_path:
        return image_path
    
    # تانياً: لو API فشل، نجيب صورة محلية
    logger.info(f"📁 Trying local images for type: {post_type}")
    local_image = get_random_local_image(post_type)
    
    if local_image:
        logger.info(f"✅ Using local image: {local_image}")
        return local_image
    
    # تالتاً: لو مفيش صور خالص، ننشر بدون صورة
    logger.warning(f"⚠️ No image found for type: {post_type}, posting without image")
    return None