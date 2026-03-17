import streamlit as st
import os
from dotenv import load_dotenv

# تحميل المتغيرات البيئية في بداية التطبيق
load_dotenv()

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
import integration
import json

# --- التبويبات ---
tabs = st.tabs([
    "تحليل الدومين",
    "فحص المواقع",
    "بحث عن المستخدم",
    "تحديد الموقع الجغرافي",
    "سطح الهجوم",
    "تحليل ذكي",
    "التقارير",
    "🤖 مساعد الهجوم الذكي",
    "🔎 Google Dork",
    "📧 Email OSINT",
    "📱 Phone Lookup",
    "🌑 Dark Web",
    "🔌 Port Scanner",
    "⚠️ Vulnerability Scanner",
    "🗺 Network Mapper",
    "🤖 AI Threat Analysis",
    "💡 AI Pentest Advisor"
])

st.set_page_config(page_title="CyberShield Pro OSINT", layout="wide")
st.title("🛡 منصة CyberShield Pro للذكاء الاستخباراتي و OSINT")

# ----------------------------
# تحليل الدومين
# ----------------------------
with tabs[0]:
    domain = st.text_input("أدخل اسم الدومين", key="domain_input")
    if st.button("تحليل الدومين", key="domain_btn"):
        whois = domain_osint.whois_lookup(domain)
        dns = domain_osint.dns_lookup(domain)
        subs = domain_osint.subdomain_scan(domain)
        st.write("WHOIS", whois)
        st.write("DNS", dns)
        st.write("النطاقات الفرعية المكتشفة", subs)
        st.session_state["domain"] = domain
        st.session_state["subs"] = subs

# ----------------------------
# فحص المواقع
# ----------------------------
with tabs[1]:
    url = st.text_input("أدخل رابط الموقع", key="site_input")
    if st.button("فحص الموقع", key="site_btn"):
        tech = website_scan.detect_tech(url)
        headers = website_scan.header_analysis(url)
        emails = website_scan.extract_emails(url)
        st.write("التقنيات المكتشفة", tech)
        st.write("الهيدرز", headers)
        st.write("الإيميلات المكتشفة", emails)
        st.session_state["scan"] = {"tech": tech, "headers": headers, "emails": emails}

# ----------------------------
# بحث عن المستخدم
# ----------------------------
with tabs[2]:
    username = st.text_input("أدخل اسم المستخدم", key="username_input")
    if st.button("بحث عن المستخدم", key="username_btn"):
        result = username_osint.username_search(username)
        if isinstance(result, dict) and result:
            st.success("تم العثور على الحسابات التالية:")
            for platform, link in result.items():
                st.write(f"✅ {platform} : {link}")
        else:
            st.warning("لم يتم العثور على حسابات بهذا الاسم")

# ----------------------------
# تحديد الموقع الجغرافي
# ----------------------------
with tabs[3]:
    ip = st.text_input("أدخل IP", key="geoip_input")
    if st.button("تحديد الموقع", key="geoip_btn"):
        data = geoip_osint.geoip(ip)
        st.write(data)

# ----------------------------
# سطح الهجوم
# ----------------------------
with tabs[4]:
    if "subs" in st.session_state:
        file = attack_surface.draw_graph(st.session_state["domain"], st.session_state["subs"])
        st.image(file)
    else:
        st.warning("قم أولاً بفحص النطاقات الفرعية")

# ----------------------------
# التحليل الذكي
# ----------------------------
with tabs[5]:
    if "subs" in st.session_state:
        analysis = ai_analysis.analyze_ports(
            st.session_state["domain"], list(st.session_state["subs"].values())
        )
        st.text(analysis)
    else:
        st.warning("قم أولاً بفحص النطاقات الفرعية")

# ----------------------------
# التقارير
# ----------------------------
with tabs[6]:
    if st.button("إنشاء تقرير PDF", key="report_btn"):
        file = report_generator.create_report(st.session_state)
        with open(file, "rb") as f:
            st.download_button("تحميل التقرير", f, file_name=file, key="download_report")

# ----------------------------
# مساعد الهجوم الذكي
# ----------------------------
with tabs[7]:
    target = st.text_input("🎯 أدخل الدومين أو IP للتحليل", key="ai_target_input")
    open_ports_input = st.text_input("المنافذ المفتوحة (مثال: 22,80,443)", key="ai_ports_input")
    tech_input = st.text_input("التقنيات المكتشفة (مثال: WordPress, Django)", key="ai_tech_input")
    if st.button("تحليل الهدف بالذكاء الاصطناعي", key="ai_btn"):
        open_ports = [int(p.strip()) for p in open_ports_input.split(",") if p.strip().isdigit()]
        tech_list = [t.strip() for t in tech_input.split(",") if t.strip()]
        ai_hacking_assistant = AIHackingAssistant()
        analysis = ai_hacking_assistant.analyze_target(target, open_ports, tech_list, headers=None)
        st.code(analysis)

# ----------------------------
# الأدوات الجديدة
# ----------------------------
with tabs[8]:
    query = st.text_input("أدخل نص البحث للـ Google Dork", key="dork_input")
    if st.button("بحث Google Dork", key="dork_btn"):
        results = google_dork.search_dork(query)
        if isinstance(results, dict) and "error" in results:
            st.error(results["error"])
        else:
            for r in results:
                st.markdown(f"**[{r['title']}]({r['url']})**<br>{r['snippet']}", unsafe_allow_html=True)

with tabs[9]:
    email = st.text_input("أدخل البريد الإلكتروني للتحليل", key="email_input")
    if st.button("بحث البريد الإلكتروني", key="email_btn"):
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
                else:
                    st.info("لم يتم العثور على نتائج بحث إضافية.")

with tabs[10]:
    number = st.text_input("أدخل رقم الهاتف", key="phone_input")
    if st.button("بحث رقم الهاتف", key="phone_btn"):
        res = phone_osint.phone_lookup(number)
        if isinstance(res, dict) and "error" in res:
            st.error(res["error"])
        elif isinstance(res, dict) and "message" in res:
            st.info(res["message"])
        else:
            for r in res:
                st.markdown(f"**[{r['title']}]({r['url']})**<br>{r['snippet']}", unsafe_allow_html=True)

with tabs[11]:
    query = st.text_input("أدخل نص البحث في الشبكة المظلمة", key="darkweb_input")
    if st.button("بحث Dark Web", key="darkweb_btn"):
        res = darkweb_search.darkweb_lookup(query)
        if isinstance(res, dict) and "error" in res:
            st.error(res["error"])
        elif isinstance(res, dict) and "message" in res:
            st.info(res["message"])
        else:
            for r in res:
                st.markdown(f"**[{r['title']}]({r['url']})**<br>{r['snippet']}", unsafe_allow_html=True)

with tabs[12]:
    target_port = st.text_input("أدخل IP أو الدومين للفحص", key="port_input")
    if st.button("فحص المنافذ", key="port_btn"):
        res = port_scanner.scan_ports(target_port)
        st.write(res)

with tabs[13]:
    target_vuln = st.text_input("أدخل IP أو الدومين للفحص", key="vuln_input")
    if st.button("فحص الثغرات", key="vuln_btn"):
        res = vuln_scanner.scan_vulnerabilities(target_vuln)
        if isinstance(res, dict) and "error" in res:
            st.error(res["error"])
        elif isinstance(res, dict) and "message" in res:
            st.info(res["message"])
        else:
            for vuln in res:
                st.write(f"**{vuln['title']}** - [Link]({vuln['url']})<br>{vuln['snippet']}")

with tabs[14]:
    target_net = st.text_input("أدخل IP أو الدومين لرسم الشبكة", key="net_input")
    if st.button("رسم الشبكة", key="net_btn"):
        file = network_mapper.map_network(target_net)
        st.image(file)

with tabs[15]:
    target_threat = st.text_input("أدخل الهدف لتحليل التهديدات", key="threat_input")
    if st.button("تحليل التهديد", key="threat_btn"):
        res = ai_threat.analyze_threat(target_threat)
        st.write(res)

with tabs[16]:
    target_pentest = st.text_input("أدخل الهدف لاختبار الاختراق", key="pentest_target_input")
    open_ports_input = st.text_input("المنافذ المفتوحة (مثال: 22,80,443)", key="pentest_ports_input")
    tech_input = st.text_input("التقنيات المكتشفة (مثال: WordPress, Django)", key="pentest_tech_input")
    if st.button("اقتراح اختبار اختراق", key="pentest_btn"):
        open_ports = [int(p.strip()) for p in open_ports_input.split(",") if p.strip().isdigit()]
        tech_list = [t.strip() for t in tech_input.split(",") if t.strip()]
        res = ai_pentest.pentest_advice(target_pentest, open_ports, tech_list)
        st.write(res)
