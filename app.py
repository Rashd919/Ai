import streamlit as st
import os
import io
import json
from dotenv import load_dotenv

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
from ai_hacking import AIHackingAssistant

# إعداد الصفحة
st.set_page_config(page_title="CyberShield Pro OSINT", layout="wide", page_icon="🛡️")

# تحميل .env (لو موجود)
load_dotenv()

# --- الشريط الجانبي للإعدادات ---
with st.sidebar:
    st.title("⚙️ الإعدادات")
    st.info("يمكنك إدخال مفاتيح API هنا إذا لم تكن مضافة في Secrets")
    
    groq_key = st.text_input("GROQ API KEY", type="password", value=config.get_key("GROQ_API_KEY") or "")
    if groq_key:
        st.session_state["GROQ_API_KEY"] = groq_key
        
    tavily_key = st.text_input("TAVILY API KEY", type="password", value=config.get_key("TAVILY_API_KEY") or "")
    if tavily_key:
        st.session_state["TAVILY_API_KEY"] = tavily_key

    st.divider()
    st.markdown("### 🛠️ حالة النظام")
    if config.get_key("GROQ_API_KEY"):
        st.success("✅ Groq API: متصل")
    else:
        st.error("❌ Groq API: غير متصل")
        
    if config.get_key("TAVILY_API_KEY"):
        st.success("✅ Tavily API: متصل")
    else:
        st.error("❌ Tavily API: غير متصل")

st.title("🛡️ منصة CyberShield Pro للذكاء الاستخباراتي و OSINT")

# --- التبويبات ---
tabs = st.tabs([
    "🌐 تحليل الدومين",
    "🔍 فحص المواقع",
    "👤 بحث عن المستخدم",
    "📍 الموقع الجغرافي",
    "🏗️ سطح الهجوم",
    "🧠 تحليل ذكي",
    "🤖 مساعد الهجوم",
    "🔎 Google Dork",
    "📧 Email OSINT",
    "📱 Phone Lookup",
    "🌑 Dark Web",
    "🔌 Port Scanner",
    "⚠️ Vulnerabilities",
    "🗺️ Network Mapper",
    "🚨 AI Threat",
    "💡 AI Pentest",
    "📄 التقارير"
])

# 1. تحليل الدومين
with tabs[0]:
    domain = st.text_input("أدخل اسم الدومين", key="domain_input_main")
    if st.button("تحليل الدومين", key="domain_btn_main"):
        with st.spinner("جاري التحليل..."):
            whois = domain_osint.whois_lookup(domain)
            dns = domain_osint.dns_lookup(domain)
            subs = domain_osint.subdomain_scan(domain)
            st.subheader("WHOIS Data")
            st.write(whois)
            st.subheader("DNS Records")
            st.write(dns)
            st.subheader("Subdomains")
            st.write(subs)
            st.session_state["domain"] = domain
            st.session_state["subs"] = subs

# 2. فحص المواقع
with tabs[1]:
    url = st.text_input("أدخل رابط الموقع", key="site_input_main")
    if st.button("فحص الموقع", key="site_btn_main"):
        with st.spinner("جاري الفحص..."):
            tech = website_scan.detect_tech(url)
            headers = website_scan.header_analysis(url)
            emails = website_scan.extract_emails(url)
            st.write("### التقنيات المكتشفة", tech)
            st.write("### الهيدرز", headers)
            st.write("### الإيميلات المكتشفة", emails)
            st.session_state["scan"] = {"tech": tech, "headers": headers, "emails": emails}

# 3. بحث عن المستخدم
with tabs[2]:
    username = st.text_input("أدخل اسم المستخدم", key="username_input_main")
    if st.button("بحث عن المستخدم", key="username_btn_main"):
        with st.spinner("جاري البحث..."):
            result = username_osint.username_search(username)
            if isinstance(result, dict) and result:
                st.success(f"تم العثور على حسابات لـ {username}:")
                for platform, link in result.items():
                    st.markdown(f"✅ **{platform}**: [زيارة الحساب]({link})")
            else:
                st.warning("لم يتم العثور على حسابات بهذا الاسم")

# 4. تحديد الموقع الجغرافي
with tabs[3]:
    ip = st.text_input("أدخل IP", key="geoip_input_main")
    if st.button("تحديد الموقع", key="geoip_btn_main"):
        data = geoip_osint.geoip(ip)
        st.json(data)

# 5. سطح الهجوم
with tabs[4]:
    if "subs" in st.session_state and st.session_state["subs"]:
        with st.spinner("جاري رسم سطح الهجوم..."):
            file = attack_surface.draw_graph(st.session_state.get("domain", "Target"), st.session_state["subs"])
            st.image(file, caption="خريطة سطح الهجوم")
    else:
        st.warning("⚠️ يرجى إجراء 'تحليل الدومين' أولاً للحصول على النطاقات الفرعية.")

# 6. التحليل الذكي
with tabs[5]:
    if "subs" in st.session_state and st.session_state["subs"]:
        with st.spinner("جاري التحليل بالذكاء الاصطناعي..."):
            analysis = ai_analysis.analyze_ports(
                st.session_state.get("domain", "Target"), 
                list(st.session_state["subs"].values()) if isinstance(st.session_state["subs"], dict) else []
            )
            st.markdown(analysis)
    else:
        st.warning("⚠️ يرجى إجراء 'تحليل الدومين' أولاً.")

# 7. مساعد الهجوم الذكي
with tabs[6]:
    st.subheader("🤖 مساعد الهجوم الذكي (Groq AI)")
    target_ai = st.text_input("🎯 الدومين أو IP", key="ai_target_input_main")
    ports_ai = st.text_input("المنافذ (مثال: 80, 443)", key="ai_ports_input_main")
    tech_ai = st.text_input("التقنيات (مثال: WordPress)", key="ai_tech_input_main")
    if st.button("تحليل الهدف", key="ai_btn_main"):
        with st.spinner("جاري التحليل..."):
            open_ports = [int(p.strip()) for p in ports_ai.split(",") if p.strip().isdigit()]
            ai_assistant = AIHackingAssistant()
            res = ai_assistant.analyze_target(target_ai, open_ports, tech_ai)
            st.markdown(res)

# 8. Google Dork
with tabs[7]:
    dork_query = st.text_input("أدخل نص البحث (Dork)", key="dork_input_main")
    if st.button("بحث Dork", key="dork_btn_main"):
        with st.spinner("جاري البحث..."):
            results = google_dork.search_dork(dork_query)
            if isinstance(results, list):
                for r in results:
                    st.markdown(f"🔗 **[{r['title']}]({r['url']})**")
                    st.caption(r['snippet'])
                    st.divider()
            else:
                st.error(results.get("error", "حدث خطأ ما"))

# 9. Email OSINT
with tabs[8]:
    email_target = st.text_input("أدخل البريد الإلكتروني", key="email_input_main")
    if st.button("فحص البريد", key="email_btn_main"):
        with st.spinner("جاري البحث عن تسريبات..."):
            res = email_osint.email_search(email_target)
            if "error" in res:
                st.error(res["error"])
            else:
                if "Tavily_Analysis" in res:
                    st.markdown("### 🧠 تحليل الذكاء الاصطناعي")
                    st.write(res["Tavily_Analysis"])
                if "Search_Results" in res:
                    st.markdown("### 🔗 نتائج البحث")
                    for r in res["Search_Results"]:
                        st.markdown(f"**[{r['title']}]({r['url']})**")
                        st.caption(r['snippet'])

# 10. Phone Lookup
with tabs[9]:
    phone_target = st.text_input("أدخل رقم الهاتف (مع رمز الدولة)", key="phone_input_main")
    if st.button("بحث الهاتف", key="phone_btn_main"):
        with st.spinner("جاري البحث..."):
            res = phone_osint.phone_lookup(phone_target)
            if isinstance(res, list):
                for r in res:
                    st.markdown(f"📞 **[{r['title']}]({r['url']})**")
                    st.caption(r['snippet'])
            else:
                st.error(res.get("error", "لم يتم العثور على نتائج"))

# 11. Dark Web
with tabs[10]:
    dark_query = st.text_input("أدخل الكلمة المفتاحية للبحث", key="dark_input_main")
    if st.button("بحث Dark Web", key="dark_btn_main"):
        with st.spinner("جاري البحث عن تسريبات..."):
            res = darkweb_search.darkweb_lookup(dark_query)
            if isinstance(res, list):
                for r in res:
                    st.markdown(f"🌑 **[{r['title']}]({r['url']})**")
                    st.caption(r['snippet'])
            else:
                st.error(res.get("error", "لا توجد نتائج"))

# 12. Port Scanner
with tabs[11]:
    port_target = st.text_input("أدخل IP أو الدومين للفحص", key="port_input_main")
    if st.button("فحص المنافذ", key="port_btn_main"):
        with st.spinner("جاري الفحص..."):
            res = port_scanner.scan_ports(port_target)
            st.write(res)

# 13. Vulnerability Scanner
with tabs[12]:
    vuln_target = st.text_input("أدخل الهدف لفحص الثغرات", key="vuln_input_main")
    if st.button("فحص الثغرات", key="vuln_btn_main"):
        with st.spinner("جاري البحث عن ثغرات معروفة..."):
            res = vuln_scanner.scan_vulnerabilities(vuln_target)
            if isinstance(res, list):
                for v in res:
                    st.markdown(f"⚠️ **[{v['title']}]({v['url']})**")
                    st.caption(v['snippet'])
            else:
                st.error(res.get("error", "لا توجد ثغرات مكتشفة"))

# 14. Network Mapper
with tabs[13]:
    net_target = st.text_input("أدخل الهدف لرسم الشبكة", key="net_input_main")
    if st.button("رسم الشبكة", key="net_btn_main"):
        with st.spinner("جاري الرسم..."):
            res = network_mapper.map_network(net_target)
            if isinstance(res, io.BytesIO):
                st.image(res, caption=f"خريطة الشبكة لـ {net_target}")
            else:
                st.error(res)

# 15. AI Threat Analysis
with tabs[14]:
    threat_target = st.text_input("أدخل الهدف لتحليل التهديدات", key="threat_input_main")
    if st.button("تحليل التهديدات", key="threat_btn_main"):
        with st.spinner("جاري التحليل..."):
            res = ai_threat.analyze_threat(threat_target)
            st.markdown(res)

# 16. AI Pentest Advisor
with tabs[15]:
    pentest_target = st.text_input("أدخل الهدف لاقتراح خطة اختراق", key="pentest_input_main")
    if st.button("اقتراح خطة", key="pentest_btn_main"):
        with st.spinner("جاري إعداد الخطة..."):
            res = ai_pentest.pentest_advice(pentest_target, [], "Unknown")
            st.markdown(res)

# 17. التقارير
with tabs[16]:
    st.subheader("📄 إنشاء تقرير شامل")
    if st.button("توليد تقرير PDF", key="report_btn_main"):
        if "domain" in st.session_state:
            with st.spinner("جاري إنشاء التقرير..."):
                file_path = report_generator.create_report(st.session_state)
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        st.download_button("📥 تحميل التقرير", f, file_name=os.path.basename(file_path))
                else:
                    st.error("حدث خطأ أثناء إنشاء ملف التقرير")
        else:
            st.warning("⚠️ يرجى إجراء بعض الفحوصات أولاً لتضمينها في التقرير.")
