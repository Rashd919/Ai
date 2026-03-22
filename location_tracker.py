import random
import string

def generate_tracking_link(base_url="https://iplogger.org/"):
    """
    توليد رابط تتبع (محاكاة لروابط التتبع الاحترافية).
    في الواقع، يتطلب هذا خدمات خارجية مثل IPLogger أو Grabify.
    """
    # توليد كود عشوائي للرابط
    random_code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    # أمثلة لروابط تتبع مشهورة
    trackers = [
        f"https://grabify.link/{random_code}",
        f"https://iplogger.org/2t{random_code}",
        f"https://blasze.com/{random_code}"
    ]
    
    return random.choice(trackers)

def get_tracking_instructions():
    return """
    ### 📍 كيفية الحصول على الموقع الدقيق (GPS):
    1. قم بتوليد رابط تتبع من الأسفل.
    2. أرسل الرابط للهدف (مثلاً كصورة أو مقال مشوق).
    3. بمجرد ضغط الهدف على الرابط، سيقوم الموقع بتسجيل:
       - **إحداثيات GPS الدقيقة** (إذا وافق على إذن الموقع).
       - **عنوان IP الحقيقي**.
       - **نوع الجهاز والمتصفح**.
    4. يمكنك متابعة النتائج من خلال لوحة تحكم الموقع المزود للخدمة.
    """
