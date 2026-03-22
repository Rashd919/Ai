import random
import string

def generate_tracking_link():
    """
    توليد رابط تتبع ورابط لوحة تحكم (محاكاة لخدمات Grabify/IPLogger).
    """
    # كود عشوائي للرابط
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    # رابط التتبع (الذي يرسل للهدف)
    tracking_url = f"https://grabify.link/{code}"
    
    # رابط لوحة التحكم (الذي يفتحه المستخدم لرؤية النتائج)
    log_url = f"https://grabify.link/track/{code}"
    
    return {
        "tracking_url": tracking_url,
        "log_url": log_url,
        "code": code
    }

def get_tracking_instructions():
    return """
    ### 📍 دليل استخدام نظام التتبع:
    
    1.  **رابط التتبع (Target Link):** هذا هو الرابط الذي يجب أن ترسل للهدف (مثلاً كصورة أو مقال).
    2.  **لوحة التحكم (Tracking Log):** هذا الرابط خاص بك **أنت فقط**. افتحه لترى:
        *   **إحداثيات GPS الدقيقة** (إذا وافق الهدف).
        *   **عنوان IP الحقيقي** ومزود الخدمة.
        *   **نوع الجهاز** (آيفون، أندرويد، ويندوز).
        *   **المتصفح واللغة**.
    
    ⚠️ **ملاحظة:** للحصول على أدق النتائج، يفضل إرسال الرابط كـ "صورة" أو "فيديو" لجذب الهدف للضغط.
    """
