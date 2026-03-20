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
# بدائل في حال الحاجة: "llama3-8b-8192", "mixtral-8x7b-32768"
