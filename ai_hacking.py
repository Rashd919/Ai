import random
import os
from groq import Groq
import json

class AIHackingAssistant:
    def __init__(self):
        self.name = "CyberShield AI Hacking Assistant"
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama3-8b-8192" # أو أي نموذج Groq آخر تفضله

    def analyze_target(self, domain, open_ports=None, tech=None, headers=None):
        """
        تحليل كامل للهدف باستخدام LLM (Groq):
        - المنافذ المفتوحة
        - التقنيات المستخدمة
        - الهيدرز الأمنية
        """
        prompt = f"أنت مساعد خبير في الأمن السيبراني. قم بتحليل الهدف التالي: {domain}.\n\n"
        if open_ports:
            prompt += f"المنافذ المفتوحة: {", ".join(map(str, open_ports))}.\n"
        if tech:
            prompt += f"التقنيات المكتشفة: {", ".join(tech)}.\n"
        if headers:
            prompt += f"الهيدرز الأمنية: {json.dumps(headers)}.\n"
        
        prompt += "\nبناءً على هذه المعلومات، قدم تقريرًا مفصلاً يتضمن:\n"
        prompt += "1. ملخصًا للوضع الأمني.\n"
        prompt += "2. الثغرات المحتملة بناءً على المنافذ والتقنيات.\n"
        prompt += "3. اقتراحات محددة للهجوم (إذا كان الهدف اختبار اختراق) أو للحماية (إذا كان الهدف تحصين)."
        prompt += "4. درجة خطورة عامة (منخفضة، متوسطة، عالية، حرجة)."

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "أنت مساعد خبير في الأمن السيبراني."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=1500
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"خطأ في تحليل الذكاء الاصطناعي (Groq): {str(e)}"

# تهيئة وحدة الذكاء الاصطناعي الجاهزة للاستخدام
ai_hacking = AIHackingAssistant()
