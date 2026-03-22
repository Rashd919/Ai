import os
import requests
import base64
from groq import Groq
import config

class AIChatAssistant:
    def __init__(self):
        self.api_key = config.get_key("GROQ_API_KEY")
        self.github_token = config.get_key("GITHUB_TOKEN")
        self.repo_name = config.REPO_NAME
        self.client = Groq(api_key=self.api_key) if self.api_key else None

    def chat(self, message, history=[]):
        """
        إجراء محادثة مع الذكاء الاصطناعي مع القدرة على فهم طلبات تعديل GitHub.
        """
        if not self.client:
            return "⚠️ عذراً، مفتاح GROQ_API_KEY غير متوفر."

        # بناء سياق المحادثة
        messages = [
            {"role": "system", "content": "أنت مساعد أمني ذكي وخبير في البرمجة. يمكنك مساعدة المستخدم في تحليل الأهداف الأمنية أو تعديل كود المشروع الخاص به على GitHub. إذا طلب المستخدم تعديل ملف، اطلب منه التفاصيل بوضوح."}
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
        """
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
