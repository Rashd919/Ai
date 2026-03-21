import os
from groq import Groq
import config

def analyze_ports(domain, open_ports):
    """
    تحليل المنافذ المفتوحة بأسلوب دفاعي ومختصر.
    """
    api_key = config.get_key("GROQ_API_KEY")
    if not api_key:
        return "⚠️ خطأ: GROQ_API_KEY غير موجود."

    try:
        client = Groq(api_key=api_key)
        model = config.GROQ_MODEL

        prompt = f"""
        أنت خبير في التحليل الأمني الدفاعي. قم بتحليل المنافذ المفتوحة التالية للهدف {domain}:
        المنافذ: {', '.join(map(str, open_ports)) if open_ports else 'لا توجد منافذ مفتوحة'}

        المطلوب:
        1. ملخص أمني سريع (Quick Security Summary).
        2. المخاطر المرتبطة بهذه المنافذ (Associated Risks).
        3. خطوات التحصين (Hardening Steps).

        اجعل الإجابة باللغة العربية، مختصرة جداً، ومباشرة.
        """

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "أنت محلل أمني دفاعي خبير. إجاباتك تقنية، مختصرة، ومباشرة."},
                {"role": "user", "content": prompt}
            ],
            model=model,
            temperature=0.5,
            max_tokens=600
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"❌ خطأ في تحليل المنافذ: {str(e)}"
