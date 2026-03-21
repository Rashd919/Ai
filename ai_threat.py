import os
from groq import Groq
import config

def analyze_threat(target):
    """
    تحليل التهديدات الذكي بأسلوب دفاعي ومختصر.
    """
    api_key = config.get_key("GROQ_API_KEY")
    if not api_key:
        return "⚠️ خطأ: GROQ_API_KEY غير موجود."

    try:
        client = Groq(api_key=api_key)
        model = config.GROQ_MODEL

        prompt = f"""
        أنت خبير في تحليل التهديدات الأمنية. قم بتحليل التهديدات المحتملة للهدف: {target}.
        
        المطلوب: تقديم تقرير أمني مختصر جداً ومباشر (نقاط واضحة):
        1. أنواع التهديدات المحتملة (Potential Threats).
        2. مستوى الخطورة (Risk Level).
        3. توصيات التخفيف (Mitigation Recommendations).

        اجعل الإجابة باللغة العربية، مختصرة جداً، ومباشرة.
        """

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "أنت خبير في تحليل التهديدات الأمنية. إجاباتك دائماً تقنية، مباشرة، ومختصرة."},
                {"role": "user", "content": prompt}
            ],
            model=model,
            temperature=0.5,
            max_tokens=600
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"❌ خطأ في تحليل التهديدات: {str(e)}"
