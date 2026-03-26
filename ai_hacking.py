import os
from groq import Groq
import json
import config

class AIHackingAssistant:
    def __init__(self):
        self.name = "CyberShield AI Security Assistant"
        self.model = config.GROQ_MODEL

    def chat(self, user_input):
        # محاولة استخدام Groq أولاً
        groq_key = config.get_key("GROQ_API_KEY")
        if groq_key:
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
                if "organization_restricted" in str(e).lower() or "400" in str(e):
                    pass # الانتقال لـ Gemini في حال وجود قيود على Groq
                else:
                    return f"❌ خطأ في Groq: {str(e)}"

        # محاولة استخدام Gemini كبديل (Fallback)
        gemini_key = config.get_key("GEMINI_API_KEY")
        if gemini_key:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemini_key}"
                payload = {
                    "contents": [{"parts": [{"text": f"أنت Rashd_Ai، مساعد ذكي متخصص في الأمن السيبراني. أجب باللغة العربية باحترافية واختصار على: {user_input}"}]}]
                }
                response = requests.post(url, json=payload, timeout=10)
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            except Exception as ge:
                return f"❌ خطأ في الاتصال بكافة المحركات: {str(ge)}"
        
        return "⚠️ خطأ: لا توجد مفاتيح API صالحة للذكاء الاصطناعي."

    def analyze_target(self, domain, open_ports=None, tech=None, headers=None):
        api_key = config.get_key("GROQ_API_KEY")
        if not api_key:
            return "⚠️ خطأ: GROQ_API_KEY غير موجود."

        try:
            client = Groq(api_key=api_key)
            prompt = f"""
            أنت خبير في الأمن السيبراني والتحليل الدفاعي. قم بتحليل البيانات التالية للهدف: {domain}
            البيانات المتاحة:
            - المنافذ: {', '.join(map(str, open_ports)) if open_ports else 'غير محددة'}
            - التقنيات: {tech if tech else 'غير محددة'}
            - الهيدرز: {json.dumps(headers) if headers else 'غير محددة'}
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
