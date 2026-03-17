from groq import Groq
from config import get_key

def analyze_threat(target):
    """
    تحليل التهديدات الذكي باستخدام LLM (Groq).
    """

    try:
        api_key = get_key("GROQ_API_KEY")
        client = Groq(api_key=api_key)
    except Exception as e:
        return f"❌ مشكلة في API KEY: {str(e)}"

    model = "llama3-8b-8192"

    prompt = f"أنت خبير في تحليل التهديدات الأمنية. قم بتحليل التهديدات المحتملة للهدف: {target}.\n\n"
    prompt += "قدم تقريرًا مفصلاً يتضمن:\n"
    prompt += "1. أنواع التهديدات المحتملة التي قد تواجه هذا الهدف.\n"
    prompt += "2. مستوى الخطورة لكل تهديد (منخفض، متوسط، عالٍ، حرج).\n"
    prompt += "3. توصيات محددة للتخفيف من هذه التهديدات وحماية الهدف.\n"

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "أنت خبير في تحليل التهديدات الأمنية."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model,
            temperature=0.7,
            max_tokens=1500
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"خطأ في تحليل التهديدات (Groq): {str(e)}"
