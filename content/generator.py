# content/generator.py

import google.genai as genai
from google.genai import types
from config.settings import settings
from content.prompts import get_prompt
from utils.logger import logger
from utils.helpers import format_post_text

client = None

def setup_gemini():
    global client
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    logger.info("✅ Gemini API configured successfully")


def generate_post(post_type: str) -> str:
    try:
        logger.info(f"🤖 Generating post for type: {post_type}")

        system_prompt, user_prompt = get_prompt(post_type)

        # بنضيف تعليمات صريحة إن البوست لازم يكون مكتمل
        final_prompt = f"""
{user_prompt}

تعليمات إضافية مهمة جداً:
- اكتب البوست كامل ومكتمل من أول كلمة لآخر كلمة
- لا تقطع الكلام أو تتوقف في النص
- لازم البوست ينتهي بجملة ختامية واضحة ومكتملة
- لو البوست محتاج سؤال في الآخر، اكتبه كامل
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.9,
                max_output_tokens=2048,
                top_p=0.95,
            ),
            contents=final_prompt
        )

        if not response.text:
            raise ValueError("Empty response from Gemini")

        post_text = format_post_text(response.text)

        # بنتأكد إن البوست مكتمل
        # لو بيخلص بكلمة ناقصة نعمل retry
        incomplete_endings = [
            "المهم هنا",
            "وبعدين",
            "لأن",
            "عشان",
            "بس",
            "لو",
            "وإنت",
            "وانت",
        ]

        for ending in incomplete_endings:
            if post_text.strip().endswith(ending):
                logger.warning(f"⚠️ Post seems incomplete, retrying...")
                return generate_post(post_type)

        logger.info(f"✅ Post generated ({len(post_text)} chars)")
        logger.debug(f"Post content:\n{post_text}")

        return post_text

    except ValueError as e:
        logger.error(f"❌ Value error: {e}")
        raise

    except RecursionError:
        logger.error("❌ Max retries reached for post generation")
        raise Exception("Failed to generate complete post after multiple retries")

    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        raise