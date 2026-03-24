import os
import requests
import base64
from groq import Groq
import config
import streamlit as st

class AIChatAssistant:
    def __init__(self, is_developer=False):
        self.api_key = config.get_key("GROQ_API_KEY")
        self.github_token = config.get_key("GITHUB_TOKEN")
        self.repo_name = config.REPO_NAME
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        self.is_developer = is_developer

    def chat(self, message, history=[]):
        """
        إجراء محادثة مع الذكاء الاصطناعي مع القدرة على فهم طلبات تعديل GitHub.
        """
        if not self.client:
            return "⚠️ عذراً، مفتاح GROQ_API_KEY غير متوفر."

        # التحقق من محاولات الزوار تعديل الكود
        if not self.is_developer:
            # فحص الكلمات المفتاحية التي تشير إلى محاولات تعديل الكود
            forbidden_keywords = ["تعديل", "edit", "modify", "update", "github", "code", "كود", "ملف", "file", "script", "delete", "حذف", "remove", "create", "إنشاء"]
            message_lower = message.lower()
            
            for keyword in forbidden_keywords:
                if keyword in message_lower:
                    return f"""🔐 **تنبيه أمني**: 
أنا ذكاء اصطناعي مطور من قبل **راشد أبو سعود**، وأنا تحت أمره وسيطرته الكاملة.

لا يمكنك تعديل الكود أو الوصول إلى الملفات الحساسة من هذه النسخة. هذه الصلاحيات حصرية لـ **راشد أبو سعود** فقط.

إذا كنت تريد طلب تحسينات أو تعديلات، يرجى التواصل مع **راشد أبو سعود** مباشرة."""

        # بناء سياق المحادثة بناءً على نوع المستخدم
        if self.is_developer:
            system_message = f"""أنت مساعد أمني ذكي وخبير في البرمجة، مطور من قبل **راشد أبو سعود**. أنت تحت أمره وسيطرته الكاملة.

يمكنك مساعدة **راشد أبو سعود** في:
- تحليل الأهداف الأمنية
- تعديل كود المشروع الخاص به على GitHub
- تطوير ميزات جديدة
- إصلاح الأخطاء والثغرات

في كل رد، ذكّر أنك تحت أمر وسيطرة **راشد أبو سعود**."""
        else:
            system_message = f"""أنت مساعد أمني ذكي وخبير في البرمجة، مطور من قبل **راشد أبو سعود**. أنا تحت أمره وسيطرته الكاملة.

يمكنك مساعدة المستخدم في:
- الأسئلة الأمنية العامة
- شرح المفاهيم الأمنية
- تقديم نصائح حول الحماية

لكن لا يمكنك تعديل الكود أو الوصول إلى الملفات الحساسة."""

        messages = [
            {"role": "system", "content": system_message}
        ]
        for h in history:
            messages.append({"role": h["role"], "content": h["content"]})
        messages.append({"role": "user", "content": message})

        try:
            completion = self.client.chat.completions.create(
                model=config.GROQ_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"❌ خطأ في المحادثة: {str(e)}"

    def update_github_file(self, file_path, content, commit_message="Update via AI Assistant"):
        """
        تعديل ملف في مستودع GitHub الخاص بالمستخدم.
        (متاح فقط للمطور)
        """
        if not self.is_developer:
            return "🔐 هذه الصلاحية حصرية للمطور فقط!"
        
        if not self.github_token:
            return "⚠️ عذراً، GITHUB_TOKEN غير متوفر."

        url = f"https://api.github.com/repos/{self.repo_name}/contents/{file_path}"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

        # جلب الـ SHA للملف الحالي (إذا كان موجوداً)
        res = requests.get(url, headers=headers)
        sha = None
        if res.status_code == 200:
            sha = res.json().get("sha")

        # تشفير المحتوى بـ Base64
        encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")

        data = {
            "message": commit_message,
            "content": encoded_content,
            "sha": sha
        }

        res = requests.put(url, headers=headers, json=data)
        if res.status_code in [200, 201]:
            return f"✅ تم تحديث الملف `{file_path}` بنجاح على GitHub."
        else:
            return f"❌ فشل تحديث الملف: {res.json().get('message')}"
