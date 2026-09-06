# publisher/facebook.py

import requests
from config.settings import settings
from utils.logger import logger


def publish_post_with_image(post_text: str, image_path: str) -> dict:
    """
    بتنشر بوست مع صورة على فيسبوك
    
    Args:
        post_text: نص البوست
        image_path: مسار الصورة
    
    Returns:
        dict: رد الـ API
    """
    
    url = f"https://graph.facebook.com/{settings.META_PAGE_ID}/photos"
    
    try:
        with open(image_path, "rb") as image_file:
            response = requests.post(
                url,
                data={
                    "message": post_text,
                    "access_token": settings.META_ACCESS_TOKEN
                },
                files={"source": image_file},
                timeout=30
            )
        
        response.raise_for_status()
        result = response.json()
        
        logger.info(f"✅ Post with image published: {result.get('id')}")
        return result
        
    except requests.Timeout:
        logger.error("❌ Timeout while publishing post with image")
        raise
        
    except requests.RequestException as e:
        logger.error(f"❌ Error publishing post with image: {e}")
        raise


def publish_post_without_image(post_text: str) -> dict:
    """
    بتنشر بوست بدون صورة على فيسبوك
    
    Args:
        post_text: نص البوست
    
    Returns:
        dict: رد الـ API
    """
    
    url = f"https://graph.facebook.com/{settings.META_PAGE_ID}/feed"
    
    try:
        response = requests.post(
            url,
            data={
                "message": post_text,
                "access_token": settings.META_ACCESS_TOKEN
            },
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        
        logger.info(f"✅ Post without image published: {result.get('id')}")
        return result
        
    except requests.Timeout:
        logger.error("❌ Timeout while publishing post without image")
        raise
        
    except requests.RequestException as e:
        logger.error(f"❌ Error publishing post without image: {e}")
        raise


def publish(post_text: str, image_path: str | None = None) -> dict:
    """
    الدالة الرئيسية للنشر
    بتحدد تلقائياً هل هتنشر مع صورة أو بدون
    
    Args:
        post_text: نص البوست
        image_path: مسار الصورة (اختياري)
    
    Returns:
        dict: رد الـ API
    """
    
    logger.info("📤 Starting publish process...")
    
    if image_path:
        logger.info(f"🖼️ Publishing with image: {image_path}")
        return publish_post_with_image(post_text, image_path)
    else:
        logger.info("📝 Publishing without image")
        return publish_post_without_image(post_text)


def verify_page_access() -> bool:
    url = "https://graph.facebook.com/me/accounts"
    
    try:
        response = requests.get(
            url,
            params={
                "access_token": settings.META_ACCESS_TOKEN,
            },
            timeout=10
        )
        
        response.raise_for_status()
        data = response.json()
        pages = data.get("data", [])
        
        if not pages:
            logger.error("❌ No pages found")
            return False
        
        for page in pages:
            logger.info(f"📄 Page: {page.get('name')} | ID: {page.get('id')}")
            
            # بناخد أول صفحة تلقائياً
            # ونحدث الـ Token والـ ID
            settings.META_ACCESS_TOKEN = page.get("access_token")
            settings.META_PAGE_ID = page.get("id")
            logger.info(f"✅ Using page: {page.get('name')}")
            return True
            
        return False
        
    except requests.RequestException as e:
        logger.error(f"❌ Page access verification failed: {e}")
        return False
    """
    بنتأكد إن الـ Access Token شغال
    وعندنا صلاحية على الصفحة
    قبل ما نبدأ أي حاجة
    
    Returns:
        bool: True لو كل حاجة تمام
    """
    
    url = f"https://graph.facebook.com/{settings.META_PAGE_ID}"
    
    try:
        response = requests.get(
            url,
            params={
                "access_token": settings.META_ACCESS_TOKEN,
                "fields": "name,id"
            },
            timeout=10
        )
        
        response.raise_for_status()
        data = response.json()
        
        page_name = data.get("name", "Unknown")
        logger.info(f"✅ Page access verified: {page_name}")
        return True
        
    except requests.RequestException as e:
        logger.error(f"❌ Page access verification failed: {e}")
        return False