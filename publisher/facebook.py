# publisher/facebook.py

import requests
from config.settings import settings
from utils.logger import logger


def verify_page_access() -> bool:
    """
    بنتأكد إن الـ Page Token شغال
    بدون ما نجيب token جديد
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


def publish_post_with_image(post_text: str, image_path: str) -> dict:
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

    except requests.RequestException as e:
        logger.error(f"❌ Error publishing with image: {e}")
        raise


def publish_post_without_image(post_text: str) -> dict:
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

        logger.info(f"✅ Post published: {result.get('id')}")
        return result

    except requests.RequestException as e:
        logger.error(f"❌ Error publishing: {e}")
        raise


def publish(post_text: str, image_path: str | None = None) -> dict:
    logger.info("📤 Starting publish process...")

    if image_path:
        logger.info(f"🖼️ Publishing with image: {image_path}")
        return publish_post_with_image(post_text, image_path)
    else:
        logger.info("📝 Publishing without image")
        return publish_post_without_image(post_text)