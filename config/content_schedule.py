from datetime import datetime

# جدول المحتوى الأسبوعي
# كل يوم ليه نوع بوست مختلف
CONTENT_SCHEDULE = {
    0: "تعليمي",      # الاثنين
    1: "شخصي",        # الثلاثاء
    2: "نصيحة",       # الأربعاء
    3: "تفاعلي",      # الخميس
    4: "منتج",        # الجمعة
    5: "سؤال_شائع",   # السبت
    6: "محفز",        # الأحد
}

def get_today_post_type() -> str:
    """
    بترجع نوع البوست المناسب لليوم ده
    مثلاً لو النهارده الاثنين هترجع "تعليمي"
    """
    day = datetime.now().weekday()
    post_type = CONTENT_SCHEDULE[day]
    print(f"📅 Today is day {day}, post type: {post_type}")
    return post_type