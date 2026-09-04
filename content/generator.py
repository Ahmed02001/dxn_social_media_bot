# content/generator.py

import google.generativeai as genai
from config.settings import settings
from content.prompts import get_prompt
from utils.logger import logger
from utils.helpers import format_post_text


def setup_gemini():
    """
    بنعمل setup للـ Gemini API
    بنستدعيها مرة واحدة بس في البداية
    """
    genai.configure(api_key=settings.GEMINI_API_KEY)
    logger.info("✅ Gemini API configured successfully")


def generate_post(post_type: str) -> str:
    """
    بتولد نص البوست باستخدام Gemini
    
    Args:
        post_type: نوع البوست (تعليمي، شخصي، إلخ)
    
    Returns:
        str: نص البوست الجاهز للنشر
    """
    try:
        logger.info(f"🤖 Generating post for type: {post_type}")
        
        # بنجيب الـ prompts المناسبة
        system_prompt, user_prompt = get_prompt(post_type)
        
        # بنعمل الموديل
        model = genai.GenerativeModel(
            model_name="gemini-pro",
            system_instruction=system_prompt
        )
        
        # بنولد المحتوى
        response = model.generate_content(
            user_prompt,
            generation_config={
                # بنتحكم في الإبداعية
                # 0.7 = توازن بين الإبداع والدقة
                "temperature": 0.7,
                
                # الحد الأقصى للكلمات
                "max_output_tokens": 500,
                
                # بنضمن تنوع في الردود
                "top_p": 0.9,
                "top_k": 40
            }
        )
        
        # بنتأكد إن في رد
        if not response.text:
            raise ValueError("Empty response from Gemini")
        
        # بننظف النص
        post_text = format_post_text(response.text)
        
        logger.info(f"✅ Post generated successfully ({len(post_text)} chars)")
        logger.debug(f"Post content:\n{post_text}")
        
        return post_text
        
    except ValueError as e:
        logger.error(f"❌ Value error in generate_post: {e}")
        raise
        
    except Exception as e:
        logger.error(f"❌ Unexpected error in generate_post: {e}")
        raise