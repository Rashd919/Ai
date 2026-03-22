import streamlit as st
import os
import io
import json
from dotenv import load_dotenv
from PIL import Image
import base64

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
import attack_surface
import ai_analysis
import report_generator
import telegram_bot
from ai_hacking import AIHackingAssistant
from ai_chat import AIChatAssistant

# تحميل .env
load_dotenv()

# إعداد الصفحة مع الأيقونة المخصصة
logo_path = config.LOGO_PATH
if os.path.exists(logo_path):
    logo_img = Image.open(logo_path)
    st.set_page_config(page_title="سايبر شيلد برو", layout="wide", page_icon=logo_img)
else:
    st.set_page_config(page_title="سايبر شيلد برو", layout="wide", page_icon="🛡️")

# دالة لتحويل الصورة لـ base64 لعرضها بدون رابط قابل للضغط
def get_image_as_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- مظهر الهاكر المعرب (Matrix Style RTL) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    .stApp {{
        background-color: #0a0a0a;
        color: #00ff00;
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif !important;
    }}
    
    /* إصلاح تداخل النصوص في الشريط الجانبي */
    [data-testid="stSidebar"] {{
        background-color: #0a0a0a !important;
        border-left: 1px solid #00ff00;
        padding: 20px;
    }}
    
    [data-testid="stSidebar"] * {{
        color: #00ff00 !important;
        text-align: right !important;
        direction: rtl !important;
    }}

    /* تحسين أزرار التبويبات */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background-color: #1a1a1a;
        padding: 10px;
        border-radius: 10px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        color: #00ff00 !important;
        background-color: transparent !important;
        border: 1px solid #00ff00 !important;
        border-radius: 5px !important;
        padding: 5px 15px !important;
    }}

    /* تحسين مربعات النتائج (Alerts/Expanders) */
    .stAlert, [data-testid="stExpander"] {{
        background-color: #1a1a1a !important;
        color: #00ff00 !important;
        border: 1px solid #00ff00 !important;
        text-align: right !important;
        direction: rtl !important;
    }}
    
    /* إصلاح لون النصوص داخل المربعات */
    .stAlert p, [data-testid="stExpander"] p, [data-testid="stExpander"] span {{
        color: #00ff00 !important;
    }}

    /* تحسين أزرار الإدخال */
    .stButton>button {{
        background-color: #00ff00 !important;
        color: black !important;
        border-radius: 5px;
        border: none;
        font-weight: bold;
        width: 100%;
    }}

    /* منع الأيقونة من الفتح كصورة مستقلة */
    .logo-container img {{
        pointer-events: none;
        user-select: none;
    }}
    
    h1, h2, h3, h4, h5, h6, p, span, label, div {{
        font-family: 'Cairo', sans-serif !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- الشريط الجانبي للإعدادات ---
with st.sidebar:
    if os.path.exists(logo_path):
        img_base64 = get_image_as_base64(logo_path)
        st.markdown(f'<div class="logo-container" style="text-align:center;"><img src="data:image/png;base64,{img_base64}" width="150"></div>', unsafe_allow_html=True)
    
    st.title("⚙️ إعدادات النظام")
    
    # إدارة المفاتيح
    with st.expander("🔑 مفاتيح API"):
        groq_key = st.text_input("مفتاح GROQ", type="password", value=config.get_key("GROQ_API_KEY") or "")
        if groq_key: st.session_state["GROQ_API_KEY"] = groq_key
            
        tavily_key = st.text_input("مفتاح TAVILY", type="password", value=config.get_key("TAVILY_API_KEY") or "")
        if tavily_key: st.session_state["TAVILY_API_KEY"] = tavily_key
        
        github_token = st.text_input("توكين GITHUB", type="password", value=config.get_key("GITHUB_TOKEN") or "")
        if github_token: st.session_state["GITHUB_TOKEN"] = github_token

    with st.expander("📢 بوت تلجرام"):
        tg_token = st.text_input("توكين البوت", type="password", value=config.get_key("TELEGRAM_BOT_TOKEN") or "")
        if tg_token: st.session_state["TELEGRAM_BOT_TOKEN"] = tg_token
        
        tg_chat_id = st.text_input("معرف الدردشة (Chat ID)", value=config.get_key("TELEGRAM_CHAT_ID") or "")
        if tg_chat_id: st.session_state["TELEGRAM_CHAT_ID"] = tg_chat_id

    st.divider()
    st.markdown("### 🛠️ حالة النظام")
    if config.get_key("GROQ_API_KEY"): st.success("✅ الذكاء الاصطناعي: متصل")
    else: st.error("❌ الذكاء الاصطناعي: غير متصل")
    
    if config.get_key("TAVILY_API_KEY"): st.success("✅ محرك البحث: متصل")
    else: st.error("❌ محرك البحث: غير متصل")

st.title("🛡️ منصة سايبر شيلد برو v2.0")
st.markdown("`>> تم تهيئة النظام... تم منح الوصول...`")

# --- التبويبات المعربة ---
tabs = st.tabs([
    "💬 محادثة AI",
    "🌐 الدومين",
    "🔍 المواقع",
    "👤 المستخدم",
    "📍 الموقع الجغرافي",
    "🏗️ سطح الهجوم",
    "🧠 تحليل ذكي",
    "🤖 مساعد الهجوم",
    "🔎 جوجل دورك",
    "📧 تسريبات الإيميل",
    "📱 بحث الهاتف",
    "🌑 الدارك ويب",
    "🔌 المنافذ",
    "⚠️ الثغرات",
    "🗺️ خريطة الشبكة",
    "🚨 التهديدات",
    "💡 خطة الاختراق",
    "📄 التقارير"
])

# 0. محادثة AI وتكامل GITHUB
with tabs[0]:
    st.subheader("💬 محادثة أمنية ذكية وتحكم GITHUB")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # عرض المحادثة
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # إدخال المستخدم
    if prompt := st.chat_input("اسألني أي شيء أو اطلب تعديل ملفات GitHub..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            assistant = AIChatAssistant()
            response = assistant.chat(prompt, st.session_state.chat_history[:-1])
            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            if st.button("إرسال الإجابة لتلجرام"):
                success, msg = telegram_bot.send_telegram_message(f"🤖 رد الذكاء الاصطناعي:\n{response}")
                if success: st.success("تم الإرسال بنجاح")
                else: st.error(msg)

# 1. تحليل الدومين
with tabs[1]:
    domain = st.text_input("أدخل اسم الدومين", key="domain_input_ar")
    if st.button("بدء تحليل الدومين"):
        with st.spinner("جاري التحليل..."):
            try:
                whois = domain_osint.whois_lookup(domain)
                dns = domain_osint.dns_lookup(domain)
                subs = domain_osint.subdomain_scan(domain)
                st.subheader("بيانات WHOIS")
                st.code(whois)
                st.subheader("سجلات DNS")
                st.code(dns)
                st.subheader("النطاقات الفرعية")
                st.write(subs)
                st.session_state["domain"] = domain
                st.session_state["whois"] = whois
                st.session_state["dns"] = dns
                st.session_state["subs"] = subs
                telegram_bot.send_telegram_message(f"🌐 تم تحليل الدومين: {domain}\nتم العثور على {len(subs)} نطاق فرعي.")
            except Exception as e:
                st.error(f"خطأ: {str(e)}")

# 2. فحص المواقع
with tabs[2]:
    url = st.text_input("أدخل رابط الموقع", key="site_input_ar")
    if st.button("بدء فحص الموقع"):
        with st.spinner("جاري الفحص..."):
            try:
                tech = website_scan.detect_tech(url)
                headers = website_scan.header_analysis(url)
                emails = website_scan.extract_emails(url)
                st.write("### التقنيات المكتشفة", tech)
                st.write("### تحليل الهيدرز", headers)
                st.write("### الإيميلات المكتشفة", emails)
                st.session_state["scan"] = {"tech": tech, "headers": headers, "emails": emails}
            except Exception as e:
                st.error(f"خطأ: {str(e)}")

# 3. بحث عن المستخدم
with tabs[3]:
    username = st.text_input("أدخل اسم المستخدم", key="username_input_ar")
    if st.button("بدء البحث عن المستخدم"):
        with st.spinner("جاري البحث..."):
            try:
                result = username_osint.username_search(username)
                if result:
                    st.success(f"تم العثور على حسابات لـ {username}:")
                    for platform, link in result.items():
                        st.markdown(f"✅ **{platform}**: [زيارة الحساب]({link})")
                else:
                    st.warning("لم يتم العثور على حسابات")
            except Exception as e:
                st.error(f"خطأ: {str(e)}")

# 4. الموقع الجغرافي
with tabs[4]:
    ip = st.text_input("أدخل عنوان IP", key="geoip_input_ar")
    if st.button("تحديد الموقع الجغرافي"):
        try:
            data = geoip_osint.geoip(ip)
            st.json(data)
        except Exception as e:
            st.error(f"خطأ: {str(e)}")

# 5. سطح الهجوم
with tabs[5]:
    if "subs" in st.session_state and st.session_state["subs"]:
        with st.spinner("جاري الرسم..."):
            try:
                file = attack_surface.draw_graph(st.session_state.get("domain", "الهدف"), st.session_state["subs"])
                st.image(file, caption="خريطة سطح الهجوم")
            except Exception as e:
                st.error(f"خطأ: {str(e)}")
    else:
        st.warning("⚠️ يرجى إجراء تحليل الدومين أولاً")

# 6. التحليل الذكي
with tabs[6]:
    if "subs" in st.session_state and st.session_state["subs"]:
        with st.spinner("جاري التحليل بالذكاء الاصطناعي..."):
            try:
                analysis = ai_analysis.analyze_ports(
                    st.session_state.get("domain", "الهدف"), 
                    list(st.session_state["subs"].values()) if isinstance(st.session_state["subs"], dict) else []
                )
                st.markdown(analysis)
                st.session_state["ai_analysis"] = analysis
            except Exception as e:
                st.error(f"خطأ: {str(e)}")
    else:
        st.warning("⚠️ يرجى إجراء تحليل الدومين أولاً")

# 7. مساعد الهجوم
with tabs[7]:
    st.subheader("🤖 مساعد الهجوم الذكي")
    target_ai = st.text_input("🎯 الهدف", key="ai_target_ar")
    ports_ai = st.text_input("المنافذ (مثال: 80, 443)", key="ai_ports_ar")
    tech_ai = st.text_input("التقنيات (مثال: WordPress)", key="ai_tech_ar")
    if st.button("تحليل الهدف"):
        with st.spinner("جاري التفكير..."):
            try:
                open_ports = [int(p.strip()) for p in ports_ai.split(",") if p.strip().isdigit()]
                ai_assistant = AIHackingAssistant()
                res = ai_assistant.analyze_target(target_ai, open_ports, tech_ai)
                st.markdown(res)
            except Exception as e:
                st.error(f"خطأ: {str(e)}")

# 8. جوجل دورك
with tabs[8]:
    dork_query = st.text_input("أدخل نص البحث (Dork)", key="dork_input_ar")
    if st.button("بدء بحث دورك"):
        with st.spinner("جاري البحث..."):
            res = google_dork.search_dork(dork_query)
            if isinstance(res, list):
                for r in res:
                    st.markdown(f"🔗 **[{r['title']}]({r['url']})**")
                    st.caption(r['snippet'])
                    st.divider()
            else:
                st.error("لم يتم العثور على نتائج")

# 9. تسريبات الإيميل
with tabs[9]:
    st.subheader("📧 كاشف تسريبات البريد الإلكتروني")
    email_target = st.text_input("أدخل البريد الإلكتروني", key="email_input_ar")
    if st.button("فحص التسريبات"):
        with st.spinner("جاري البحث في قواعد بيانات التسريبات..."):
            try:
                res = email_osint.email_search(email_target)
                if "error" in res:
                    st.error(res["error"])
                else:
                    st.markdown("### 🧠 النتيجة النهائية")
                    st.info(res["Analysis"])
                    if res.get("Results"):
                        with st.expander("🔗 الأدلة المكتشفة"):
                            for r in res["Results"]:
                                st.markdown(f"**[{r['title']}]({r['url']})**")
                                st.caption(r['snippet'])
                                st.divider()
                    if "تم العثور على تسريب" in res["Analysis"]:
                        telegram_bot.send_telegram_message(f"⚠️ تم العثور على تسريب لـ {email_target}!")
            except Exception as e:
                st.error(f"خطأ: {str(e)}")

# 10. بحث الهاتف
with tabs[10]:
    phone_target = st.text_input("أدخل رقم الهاتف", key="phone_input_ar")
    if st.button("بدء بحث الهاتف"):
        with st.spinner("جاري البحث..."):
            res = phone_osint.phone_lookup(phone_target)
            if isinstance(res, list):
                for r in res:
                    st.markdown(f"📞 **[{r['title']}]({r['url']})**")
                    st.caption(r['snippet'])
                    st.divider()
            else:
                st.error("لم يتم العثور على نتائج")

# 11. الدارك ويب
with tabs[11]:
    st.subheader("🌑 البحث في أرشيف الدارك ويب")
    dark_query = st.text_input("أدخل الكلمة المفتاحية", key="dark_input_ar")
    if st.button("بدء بحث الدارك ويب"):
        with st.spinner("جاري البحث في الأرشيفات المظلمة..."):
            try:
                res = darkweb_search.darkweb_lookup(dark_query)
                if "error" in res:
                    st.error(res["error"])
                else:
                    st.markdown("### 🧠 تحليل الدارك ويب")
                    st.info(res["Analysis"])
                    if res.get("Results"):
                        with st.expander("🔗 أدلة من الدارك ويب"):
                            for r in res["Results"]:
                                st.markdown(f"🌑 **[{r['title']}]({r['url']})**")
                                st.caption(r['snippet'])
                                st.divider()
            except Exception as e:
                st.error(f"خطأ: {str(e)}")

# 12. المنافذ
with tabs[12]:
    port_target = st.text_input("أدخل IP لفحص المنافذ", key="port_input_ar")
    if st.button("بدء فحص المنافذ"):
        with st.spinner("جاري البحث عن المنافذ المفتوحة..."):
            try:
                res = port_scanner.scan_ports(port_target)
                st.markdown(res)
            except Exception as e:
                st.error(f"خطأ: {str(e)}")

# 13. الثغرات
with tabs[13]:
    vuln_target = st.text_input("أدخل الهدف لفحص الثغرات", key="vuln_input_ar")
    if st.button("بدء فحص الثغرات"):
        with st.spinner("جاري البحث عن الثغرات..."):
            res = vuln_scanner.scan_vulnerabilities(vuln_target)
            if isinstance(res, list):
                st.session_state["vulns"] = res
                for v in res:
                    st.markdown(f"⚠️ **[{v['title']}]({v['url']})**")
                    st.caption(v['snippet'])
                    st.divider()
            else:
                st.error("لم يتم العثور على ثغرات")

# 14. خريطة الشبكة
with tabs[14]:
    net_target = st.text_input("أدخل الهدف لرسم الخريطة", key="net_input_ar")
    if st.button("رسم خريطة الشبكة"):
        with st.spinner("جاري الرسم..."):
            try:
                subs = st.session_state.get("subs", {})
                res = network_mapper.map_network(net_target, subs)
                if isinstance(res, io.BytesIO):
                    st.image(res, caption=f"خريطة الشبكة الحقيقية لـ: {net_target}")
                else:
                    st.error(res)
            except Exception as e:
                st.error(f"خطأ: {str(e)}")

# 15. التهديدات
with tabs[15]:
    threat_target = st.text_input("أدخل الهدف لتحليل التهديدات", key="threat_input_ar")
    if st.button("بدء تحليل التهديدات"):
        with st.spinner("جاري التحليل..."):
            try:
                res = ai_threat.analyze_threat(threat_target)
                st.markdown(res)
            except Exception as e:
                st.error(f"خطأ: {str(e)}")

# 16. خطة الاختراق
with tabs[16]:
    pentest_target = st.text_input("أدخل الهدف لإنشاء الخطة", key="pentest_input_ar")
    if st.button("إنشاء خطة الاختراق"):
        with st.spinner("جاري التخطيط..."):
            try:
                res = ai_pentest.pentest_advice(pentest_target, [], "غير معروف")
                st.markdown(res)
            except Exception as e:
                st.error(f"خطأ: {str(e)}")

# 17. التقارير
with tabs[17]:
    st.subheader("📄 إنشاء تقرير PDF استخباراتي")
    if st.button("توليد تقرير ماتريكس"):
        if "domain" in st.session_state:
            with st.spinner("جاري التشفير والتوليد..."):
                try:
                    file_path = report_generator.create_report(st.session_state)
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as f:
                            st.download_button("📥 تحميل التقرير السري", f, file_name=os.path.basename(file_path))
                        
                        if st.button("إرسال التقرير لتلجرام"):
                            success, msg = telegram_bot.send_telegram_report(file_path)
                            if success: st.success("تم الإرسال لتلجرام")
                            else: st.error(msg)
                except Exception as e:
                    st.error(f"خطأ: {str(e)}")
        else:
            st.warning("⚠️ يرجى إجراء بعض الفحوصات أولاً")
