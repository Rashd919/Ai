import os

def get_key(key):
    # 1. البحث في متغيرات البيئة (Environment Variables)
    value = os.getenv(key)

    # 2. البحث في Streamlit Secrets (لبيئة Streamlit Cloud)
    if not value:
        try:
            import streamlit as st
            if key in st.secrets:
                value = st.secrets[key]
        except:
            pass

    # 3. البحث في st.session_state (إذا قام المستخدم بإدخال المفتاح يدوياً في الواجهة)
    if not value:
        try:
            import streamlit as st
            if key in st.session_state:
                value = st.session_state[key]
        except:
            pass

    return value

# إعدادات النماذج المدعومة حالياً في Groq
GROQ_MODEL = "llama-3.3-70b-versatile" # النموذج الأحدث والأكثر استقراراً

# إعدادات إضافية للميزات الجديدة
GITHUB_TOKEN = get_key("GITHUB_TOKEN")
TELEGRAM_BOT_TOKEN = get_key("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = get_key("TELEGRAM_CHAT_ID")
REPO_NAME = "Rashd919/Ai"
LOGO_PATH = "logo.png"
IP_API_KEY = get_key("IP_API_KEY")
VICTIMS_FILE_PATH = "victims.json"

# إعدادات نظام تسجيل الدخول
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "Rashd919")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Rashd@")
