import os
import random
from datetime import datetime

def get_random_local_image(post_type: str) -> str | None:
    """
    بترجع صورة عشوائية من الفولدر
    المناسب لنوع البوست
    لو مفيش صور بترجع None
    """
    folder = f"image/local_images/{post_type}"
    
    # لو الفولدر مش موجود
    if not os.path.exists(folder):
        return None
    
    # بنجيب كل الصور في الفولدر
    images = [
        f for f in os.listdir(folder)
        if f.endswith((".jpg", ".jpeg", ".png"))
    ]
    
    # لو مفيش صور
    if not images:
        return None
    
    # بنختار صورة عشوائية
    chosen = random.choice(images)
    return os.path.join(folder, chosen)


def create_local_image_folders():
    """
    بتعمل الفولدرات المحتاجة
    للصور المحلية لو مش موجودة
    """
    post_types = [
        "تعليمي",
        "شخصي", 
        "نصيحة",
        "تفاعلي",
        "منتج",
        "سؤال_شائع",
        "محفز"
    ]
    
    for post_type in post_types:
        folder = f"image/local_images/{post_type}"
        os.makedirs(folder, exist_ok=True)
        print(f"✅ Created folder: {folder}")


def format_post_text(text: str) -> str:
    """
    بتنظف وتنسق نص البوست
    قبل ما ينتشر
    """
    # بنشيل المسافات الزيادة
    text = text.strip()
    
    # بنتأكد إن النص مش فاضي
    if not text:
        raise ValueError("Post text is empty")
    
    return text