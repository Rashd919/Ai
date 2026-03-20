import os
from groq import Groq
import config

def analyze_threat(target):
    """
    تحليل التهديدات الذكي باستخدام LLM (Groq).
    """
    api_key = config.get_key("GROQ_API_KEY")
    if not api_key:
        return "⚠️ خطأ: GROQ_API_KEY غير موجود. يرجى إضافته في إعدادات Streamlit أو ملف .env"

    try:
        client = Groq(api_key=api_key)
        model = config.GROQ_MODEL

        prompt = f"أنت خبير في تحليل التهديدات الأمنية. قم بتحليل التهديدات المحتملة للهدف: {target}.\n\n"
        prompt += "قدم تقريرًا مفصلاً يتضمن:\n"
        prompt += "1. أنواع التهديدات المحتملة التي قد تواجه هذا الهدف.\n"
        prompt += "2. مستوى الخطورة لكل تهديد (منخفض، متوسط، عالٍ، حرج).\n"
        prompt += "3. توصيات محددة للتخفيف من هذه التهديدات وحماية الهدف.\n"

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "أنت خبير في تحليل التهديدات الأمنية."},
                {"role": "user", "content": prompt}
            ],
            model=model,
            temperature=0.7,
            max_tokens=1500
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"❌ خطأ في تحليل التهديدات بالذكاء الاصطناعي (Groq): {str(e)}"
