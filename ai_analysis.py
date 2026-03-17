import random
import os
from groq import Groq

def analyze_ports(domain, open_ports):
    """
    تحليل المنافذ المفتوحة باستخدام LLM (Groq).
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    model = "llama3-8b-8192" # أو أي نموذج Groq آخر تفضله

    prompt = f"أنت خبير في الأمن السيبراني. قم بتحليل المنافذ المفتوحة التالية للهدف {domain}:\n"
    if open_ports:
        prompt += f"المنافذ المفتوحة: {", ".join(map(str, open_ports))}.\n"
    else:
        prompt += "لا توجد منافذ مفتوحة.\n"

    prompt += "\nبناءً على هذه المعلومات، قدم تقريرًا مفصلاً يتضمن:\n"
    prompt += "1. ملخصًا للوضع الأمني المتعلق بالمنافذ.\n"
    prompt += "2. الثغرات المحتملة المرتبطة بكل منفذ.\n"
    prompt += "3. اقتراحات محددة لتحصين هذه المنافذ أو استغلالها (إذا كان الهدف اختبار اختراق)."

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "أنت خبير في الأمن السيبراني."
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
        return f"خطأ في تحليل الذكاء الاصطناعي للمنافذ (Groq): {str(e)}"
