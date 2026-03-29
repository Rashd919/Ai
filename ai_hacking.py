import os
from groq import Groq
import json
import config

class AIHackingAssistant:
    def __init__(self):
        self.name = "CyberShield AI Security Assistant"
        self.model = config.GROQ_MODEL

    def chat(self, user_input):
        # التحقق من أن الإدخال ليس فارغاً
        if not user_input or not user_input.strip():
            return "⚠️ الرجاء إدخال سؤال أو استفسار."
        
        # استخدام Groq فقط
        groq_key = config.get_key("GROQ_API_KEY")
        if not groq_key:
            return "⚠️ خطأ: GROQ_API_KEY غير موجود. يرجى إضافة المفتاح في الإعدادات."
        
        try:
            client = Groq(api_key=groq_key)
            # التحقق من أن اسم النموذج صحيح
            if not self.model or self.model.strip() == "":
                return "⚠️ خطأ: اسم النموذج غير محدد."
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "أنت Rashd_Ai، مساعد ذكي متخصص في الأمن السيبراني. إجاباتك دائماً باللغة العربية، احترافية، ومختصرة."},
                    {"role": "user", "content": user_input.strip()}
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=1000
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            error_msg = str(e)
            if "400" in error_msg:
                return "❌ خطأ 400: البيانات المرسلة غير صحيحة. تأكد من صحة المفتاح واسم النموذج."
            elif "401" in error_msg:
                return "❌ خطأ 401: المفتاح غير صحيح أو منتهي الصلاحية."
            elif "429" in error_msg:
                return "❌ خطأ 429: تم تجاوز حد الطلبات. حاول لاحقاً."
            else:
                return f"❌ خطأ في Groq: {error_msg}"

    def analyze_target(self, domain, open_ports=None, tech=None, headers=None):
        # التحقق من أن الدومين ليس فارغاً
        if not domain or not domain.strip():
            return "⚠️ الرجاء إدخال دومين أو IP للتحليل."
        
        api_key = config.get_key("GROQ_API_KEY")
        if not api_key:
            return "⚠️ خطأ: GROQ_API_KEY غير موجود. يرجى إضافة المفتاح في الإعدادات."

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
            error_msg = str(e)
            if "400" in error_msg:
                return "❌ خطأ 400: البيانات المرسلة غير صحيحة. تأكد من صحة المفتاح واسم النموذج."
            else:
                return f"❌ عذراً، واجه النظام مشكلة في التحليل: {error_msg}"

# تهيئة وحدة الذكاء الاصطناعي
ai_hacking = AIHackingAssistant()
