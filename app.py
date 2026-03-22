import streamlit as st
import os
import io
import json
from dotenv import load_dotenv
from PIL import Image

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

# إعداد الصفحة مع الأيقونة المخصصة
logo_path = config.LOGO_PATH
if os.path.exists(logo_path):
    logo_img = Image.open(logo_path)
    st.set_page_config(page_title="CyberShield Pro", layout="wide", page_icon=logo_img)
else:
    st.set_page_config(page_title="CyberShield Pro", layout="wide", page_icon="🛡️")

# تحميل .env
load_dotenv()

# --- مظهر الهاكر (Matrix Style) ---
st.markdown("""
    <style>
    .main {
        background-color: #0a0a0a;
        color: #00ff00;
    }
    .stButton>button {
        background-color: #00ff00;
        color: black;
        border-radius: 5px;
        border: none;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        background-color: #1a1a1a;
        color: #00ff00;
        border: 1px solid #00ff00;
    }
    .stTab {
        color: #00ff00;
    }
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #00ff00 !important;
        font-family: 'Courier New', Courier, monospace;
    }
    .stAlert {
        background-color: #1a1a1a;
        color: #00ff00;
        border: 1px solid #00ff00;
    }
    </style>
    """, unsafe_allow_html=True)

# --- الشريط الجانبي للإعدادات ---
with st.sidebar:
    if os.path.exists(logo_path):
        st.image(logo_path, width=150)
    st.title("⚙️ CYBER SETTINGS")
    
    # إدارة المفاتيح
    with st.expander("🔑 API KEYS"):
        groq_key = st.text_input("GROQ API KEY", type="password", value=config.get_key("GROQ_API_KEY") or "")
        if groq_key: st.session_state["GROQ_API_KEY"] = groq_key
            
        tavily_key = st.text_input("TAVILY API KEY", type="password", value=config.get_key("TAVILY_API_KEY") or "")
        if tavily_key: st.session_state["TAVILY_API_KEY"] = tavily_key
        
        github_token = st.text_input("GITHUB TOKEN", type="password", value=config.get_key("GITHUB_TOKEN") or "")
        if github_token: st.session_state["GITHUB_TOKEN"] = github_token

    with st.expander("📢 TELEGRAM BOT"):
        tg_token = st.text_input("BOT TOKEN", type="password", value=config.get_key("TELEGRAM_BOT_TOKEN") or "")
        if tg_token: st.session_state["TELEGRAM_BOT_TOKEN"] = tg_token
        
        tg_chat_id = st.text_input("CHAT ID", value=config.get_key("TELEGRAM_CHAT_ID") or "")
        if tg_chat_id: st.session_state["TELEGRAM_CHAT_ID"] = tg_chat_id

    st.divider()
    st.markdown("### 🛠️ SYSTEM STATUS")
    if config.get_key("GROQ_API_KEY"): st.success("✅ AI CORE: ONLINE")
    else: st.error("❌ AI CORE: OFFLINE")
    
    if config.get_key("TAVILY_API_KEY"): st.success("✅ SEARCH ENGINE: ONLINE")
    else: st.error("❌ SEARCH ENGINE: OFFLINE")

st.title("🛡️ CYBERSHIELD PRO v2.0")
st.markdown("`>> SYSTEM INITIALIZED... ACCESS GRANTED...`")

# --- التبويبات ---
tabs = st.tabs([
    "💬 AI CHAT",
    "🌐 DOMAIN",
    "🔍 WEBSITE",
    "👤 USER",
    "📍 GEOIP",
    "🏗️ ATTACK SURFACE",
    "🧠 AI ANALYSIS",
    "🤖 HACKING ASST",
    "🔎 GOOGLE DORK",
    "📧 EMAIL LEAKS",
    "📱 PHONE LOOKUP",
    "🌑 DARK WEB",
    "🔌 PORTS",
    "⚠️ VULNS",
    "🗺️ NETWORK",
    "🚨 THREATS",
    "💡 PENTEST",
    "📄 REPORTS"
])

# 0. AI CHAT & GITHUB INTEGRATION
with tabs[0]:
    st.subheader("💬 AI SECURITY CHAT & GITHUB CONTROL")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # عرض المحادثة
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # إدخال المستخدم
    if prompt := st.chat_input("Ask me anything or request a GitHub update..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            assistant = AIChatAssistant()
            # فحص إذا كان الطلب تعديل ملف على GitHub
            if "تعديل ملف" in prompt or "update file" in prompt.lower():
                st.info("جاري معالجة طلب تعديل GitHub...")
                # مثال بسيط: استخراج المسار والمحتوى (يمكن تحسينه بالذكاء الاصطناعي)
                # هنا سنفترض أن المستخدم سيوضح المسار والمحتوى في رسائل لاحقة أو نستخدم الذكاء الاصطناعي لاستخلاصها
                response = assistant.chat(prompt, st.session_state.chat_history[:-1])
            else:
                response = assistant.chat(prompt, st.session_state.chat_history[:-1])
            
            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            # خيار إرسال المحادثة لتلجرام
            if st.button("إرسال هذه الإجابة لتلجرام"):
                success, msg = telegram_bot.send_telegram_message(f"🤖 AI Response:\n{response}")
                if success: st.success(msg)
                else: st.error(msg)

# 1. تحليل الدومين
with tabs[1]:
    domain = st.text_input("أدخل اسم الدومين", key="domain_input")
    if st.button("تحليل الدومين"):
        with st.spinner("ANALYZING..."):
            try:
                whois = domain_osint.whois_lookup(domain)
                dns = domain_osint.dns_lookup(domain)
                subs = domain_osint.subdomain_scan(domain)
                st.subheader("WHOIS Data")
                st.code(whois)
                st.subheader("DNS Records")
                st.code(dns)
                st.subheader("Subdomains")
                st.write(subs)
                st.session_state["domain"] = domain
                st.session_state["whois"] = whois
                st.session_state["dns"] = dns
                st.session_state["subs"] = subs
                
                # تنبيه تلجرام
                telegram_bot.send_telegram_message(f"🌐 Domain Analyzed: {domain}\nFound {len(subs)} subdomains.")
            except Exception as e:
                st.error(f"ERROR: {str(e)}")

# 2. فحص المواقع
with tabs[2]:
    url = st.text_input("أدخل رابط الموقع", key="site_input")
    if st.button("فحص الموقع"):
        with st.spinner("SCANNING..."):
            try:
                tech = website_scan.detect_tech(url)
                headers = website_scan.header_analysis(url)
                emails = website_scan.extract_emails(url)
                st.write("### التقنيات المكتشفة", tech)
                st.write("### الهيدرز", headers)
                st.write("### الإيميلات المكتشفة", emails)
                st.session_state["scan"] = {"tech": tech, "headers": headers, "emails": emails}
            except Exception as e:
                st.error(f"ERROR: {str(e)}")

# 3. بحث عن المستخدم
with tabs[3]:
    username = st.text_input("أدخل اسم المستخدم", key="username_input")
    if st.button("بحث عن المستخدم"):
        with st.spinner("SEARCHING..."):
            try:
                result = username_osint.username_search(username)
                if result:
                    st.success(f"FOUND ACCOUNTS FOR {username}:")
                    for platform, link in result.items():
                        st.markdown(f"✅ **{platform}**: [VISIT]({link})")
                else:
                    st.warning("NO ACCOUNTS FOUND")
            except Exception as e:
                st.error(f"ERROR: {str(e)}")

# 4. تحديد الموقع الجغرافي
with tabs[4]:
    ip = st.text_input("أدخل IP", key="geoip_input")
    if st.button("تحديد الموقع"):
        try:
            data = geoip_osint.geoip(ip)
            st.json(data)
        except Exception as e:
            st.error(f"ERROR: {str(e)}")

# 5. سطح الهجوم
with tabs[5]:
    if "subs" in st.session_state and st.session_state["subs"]:
        with st.spinner("DRAWING..."):
            try:
                file = attack_surface.draw_graph(st.session_state.get("domain", "Target"), st.session_state["subs"])
                st.image(file, caption="ATTACK SURFACE MAP")
            except Exception as e:
                st.error(f"ERROR: {str(e)}")
    else:
        st.warning("⚠️ RUN DOMAIN ANALYSIS FIRST")

# 6. التحليل الذكي
with tabs[6]:
    if "subs" in st.session_state and st.session_state["subs"]:
        with st.spinner("AI ANALYZING..."):
            try:
                analysis = ai_analysis.analyze_ports(
                    st.session_state.get("domain", "Target"), 
                    list(st.session_state["subs"].values()) if isinstance(st.session_state["subs"], dict) else []
                )
                st.markdown(analysis)
                st.session_state["ai_analysis"] = analysis
            except Exception as e:
                st.error(f"ERROR: {str(e)}")
    else:
        st.warning("⚠️ RUN DOMAIN ANALYSIS FIRST")

# 7. مساعد الهجوم الذكي
with tabs[7]:
    st.subheader("🤖 AI HACKING ASSISTANT")
    target_ai = st.text_input("🎯 TARGET", key="ai_target")
    ports_ai = st.text_input("PORTS (e.g. 80, 443)", key="ai_ports")
    tech_ai = st.text_input("TECH (e.g. WordPress)", key="ai_tech")
    if st.button("ANALYZE TARGET"):
        with st.spinner("THINKING..."):
            try:
                open_ports = [int(p.strip()) for p in ports_ai.split(",") if p.strip().isdigit()]
                ai_assistant = AIHackingAssistant()
                res = ai_assistant.analyze_target(target_ai, open_ports, tech_ai)
                st.markdown(res)
            except Exception as e:
                st.error(f"ERROR: {str(e)}")

# 8. Google Dork
with tabs[8]:
    dork_query = st.text_input("أدخل نص البحث (Dork)", key="dork_input")
    if st.button("SEARCH DORK"):
        with st.spinner("SEARCHING..."):
            res = google_dork.search_dork(dork_query)
            if isinstance(res, list):
                for r in res:
                    st.markdown(f"🔗 **[{r['title']}]({r['url']})**")
                    st.caption(r['snippet'])
                    st.divider()
            else:
                st.error("NO RESULTS FOUND")

# 9. Email OSINT
with tabs[9]:
    st.subheader("📧 EMAIL LEAK DETECTOR")
    email_target = st.text_input("أدخل البريد الإلكتروني", key="email_input")
    if st.button("CHECK LEAKS"):
        with st.spinner("SEARCHING BREACH DATABASES..."):
            try:
                res = email_osint.email_search(email_target)
                if "error" in res:
                    st.error(res["error"])
                else:
                    st.markdown("### 🧠 FINAL VERDICT")
                    st.info(res["Analysis"])
                    if res.get("Results"):
                        with st.expander("🔗 EVIDENCE FOUND"):
                            for r in res["Results"]:
                                st.markdown(f"**[{r['title']}]({r['url']})**")
                                st.caption(r['snippet'])
                                st.divider()
                    # تنبيه تلجرام إذا وجد تسريب
                    if "تم العثور على تسريب" in res["Analysis"]:
                        telegram_bot.send_telegram_message(f"⚠️ LEAK FOUND for {email_target}!\nCheck the app for details.")
            except Exception as e:
                st.error(f"ERROR: {str(e)}")

# 10. Phone Lookup
with tabs[10]:
    phone_target = st.text_input("أدخل رقم الهاتف", key="phone_input")
    if st.button("PHONE LOOKUP"):
        with st.spinner("SEARCHING..."):
            res = phone_osint.phone_lookup(phone_target)
            if isinstance(res, list):
                for r in res:
                    st.markdown(f"📞 **[{r['title']}]({r['url']})**")
                    st.caption(r['snippet'])
                    st.divider()
            else:
                st.error("NO RESULTS")

# 11. Dark Web
with tabs[11]:
    st.subheader("🌑 DARK WEB ARCHIVE SEARCH")
    dark_query = st.text_input("أدخل الكلمة المفتاحية", key="dark_input")
    if st.button("SEARCH DARK WEB"):
        with st.spinner("SEARCHING DARK ARCHIVES..."):
            try:
                res = darkweb_search.darkweb_lookup(dark_query)
                if "error" in res:
                    st.error(res["error"])
                else:
                    st.markdown("### 🧠 DARK WEB ANALYSIS")
                    st.info(res["Analysis"])
                    if res.get("Results"):
                        with st.expander("🔗 DARK EVIDENCE"):
                            for r in res["Results"]:
                                st.markdown(f"🌑 **[{r['title']}]({r['url']})**")
                                st.caption(r['snippet'])
                                st.divider()
            except Exception as e:
                st.error(f"ERROR: {str(e)}")

# 12. Port Scanner
with tabs[12]:
    port_target = st.text_input("أدخل IP للفحص", key="port_input")
    if st.button("SCAN PORTS"):
        with st.spinner("SCANNING..."):
            try:
                res = port_scanner.scan_ports(port_target)
                st.code(res)
            except Exception as e:
                st.error(f"ERROR: {str(e)}")

# 13. Vulnerability Scanner
with tabs[13]:
    vuln_target = st.text_input("أدخل الهدف للفحص", key="vuln_input")
    if st.button("SCAN VULNS"):
        with st.spinner("SEARCHING VULNS..."):
            res = vuln_scanner.scan_vulnerabilities(vuln_target)
            if isinstance(res, list):
                st.session_state["vulns"] = res
                for v in res:
                    st.markdown(f"⚠️ **[{v['title']}]({v['url']})**")
                    st.caption(v['snippet'])
                    st.divider()
            else:
                st.error("NO VULNS FOUND")

# 14. Network Mapper
with tabs[14]:
    net_target = st.text_input("أدخل الهدف للرسم", key="net_input")
    if st.button("MAP NETWORK"):
        with st.spinner("MAPPING..."):
            try:
                res = network_mapper.map_network(net_target)
                if isinstance(res, io.BytesIO):
                    st.image(res, caption=f"NETWORK MAP: {net_target}")
                else:
                    st.error(res)
            except Exception as e:
                st.error(f"ERROR: {str(e)}")

# 15. AI Threat Analysis
with tabs[15]:
    threat_target = st.text_input("أدخل الهدف للتحليل", key="threat_input")
    if st.button("ANALYZE THREATS"):
        with st.spinner("ANALYZING..."):
            try:
                res = ai_threat.analyze_threat(threat_target)
                st.markdown(res)
            except Exception as e:
                st.error(f"ERROR: {str(e)}")

# 16. AI Pentest Advisor
with tabs[16]:
    pentest_target = st.text_input("أدخل الهدف للخطة", key="pentest_input")
    if st.button("GENERATE PLAN"):
        with st.spinner("PLANNING..."):
            try:
                res = ai_pentest.pentest_advice(pentest_target, [], "Unknown")
                st.markdown(res)
            except Exception as e:
                st.error(f"ERROR: {str(e)}")

# 17. التقارير
with tabs[17]:
    st.subheader("📄 GENERATE CLASSIFIED PDF REPORT")
    if st.button("GENERATE MATRIX REPORT"):
        if "domain" in st.session_state:
            with st.spinner("ENCRYPTING & GENERATING..."):
                try:
                    file_path = report_generator.create_report(st.session_state)
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as f:
                            st.download_button("📥 DOWNLOAD CLASSIFIED PDF", f, file_name=os.path.basename(file_path))
                        
                        # خيار إرسال التقرير لتلجرام
                        if st.button("إرسال التقرير لتلجرام"):
                            success, msg = telegram_bot.send_telegram_report(file_path)
                            if success: st.success(msg)
                            else: st.error(msg)
                except Exception as e:
                    st.error(f"ERROR: {str(e)}")
        else:
            st.warning("⚠️ RUN SOME SCANS FIRST")
