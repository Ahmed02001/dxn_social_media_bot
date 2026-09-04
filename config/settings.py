import os
from dotenv import load_dotenv

# بنحمل الـ .env
load_dotenv()

class Settings:
    # Gemini
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Meta
    META_ACCESS_TOKEN: str = os.getenv("META_ACCESS_TOKEN", "")
    META_PAGE_ID: str = os.getenv("META_PAGE_ID", "")
    
    # Image
    IMAGE_API_KEY: str = os.getenv("IMAGE_API_KEY", "")
    
    # Settings
    POST_TIME: str = os.getenv("POST_TIME", "08:00")
    
    def validate(self) -> bool:
        """
        بنتأكد إن كل الـ Keys موجودة
        قبل ما نبدأ أي حاجة
        """
        missing = []
        
        if not self.GEMINI_API_KEY:
            missing.append("GEMINI_API_KEY")
        if not self.META_ACCESS_TOKEN:
            missing.append("META_ACCESS_TOKEN")
        if not self.META_PAGE_ID:
            missing.append("META_PAGE_ID")
            
        if missing:
            print(f"❌ Missing keys: {', '.join(missing)}")
            return False
            
        print("✅ All keys are valid")
        return True

# بنعمل instance واحد بس ونستخدمه في كل المشروع
settings = Settings()