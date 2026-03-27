import os
from groq import Groq
import json
import config

class AIHackingAssistant:
    def __init__(self):
        self.name = "CyberShield AI Security Assistant"
        self.model = config.GROQ_MODEL

    def chat(self, user_input):
        # استخدام Groq فقط
        groq_key = config.get_key("GROQ_API_KEY")
        if not groq_key:
            return "⚠️ خطأ: GROQ_API_KEY غير موجود."
        
        try:
            client = Groq(api_key=groq_key)
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "أنت Rashd_Ai، مساعد ذكي متخصص في الأمن السيبراني. إجاباتك دائماً باللغة العربية، احترافية، ومختصرة."},
                    {"role": "user", "content": user_input}
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=1000
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"❌ خطأ في Groq: {str(e)}"

    def analyze_target(self, domain, open_ports=None, tech=None, headers=None):
        api_key = config.get_key("GROQ_API_KEY")
        if not api_key:
            return "⚠️ خطأ: GROQ_API_KEY غير موجود."

        try:
            client = Groq(api_key=api_key)
            prompt = f"""
            أنت خبير في الأمن السيبراني والتحليل الدفاعي. قم بتحليل البيانات التالية للهدف: {domain}
            البيانات المتاحة:
            - المنافذ: {", ".join(map(str, open_ports)) if open_ports else "غير محددة"}
            - التقنيات: {tech if tech else "غير محددة"}
            - الهيدرز: {json.dumps(headers) if headers else "غير محددة"}
            المطلوب: تقديم تقرير أمني مختصر جداً ومباشر باللغة العربية.
            """
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "أنت خبير أمن سيبراني متخصص في التحليل الدفاعي والتحصين الأمني. إجاباتك دائماً تقنية، مباشرة، ومختصرة."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.5,
                max_tokens=800
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"❌ عذراً، واجه النظام مشكلة في التحليل: {str(e)}"

# تهيئة وحدة الذكاء الاصطناعي
ai_hacking = AIHackingAssistant()
