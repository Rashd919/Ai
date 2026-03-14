# app.py
import streamlit as st
import domain_osint
import website_scan
import username_osint
import geoip_osint
import attack_surface
import ai_analysis
import report_generator
from ai_hacking import ai_hacking

st.set_page_config(page_title="CyberShield Pro OSINT", layout="wide")
st.title("🛡 منصة CyberShield Pro للذكاء الاستخباراتي و OSINT")

# --- التبويبات ---
tabs = st.tabs([
    "تحليل الدومين",
    "فحص المواقع",
    "بحث عن المستخدم",
    "تحديد الموقع الجغرافي",
    "سطح الهجوم",
    "تحليل ذكي",
    "التقارير",
    "🤖 مساعد الهجوم الذكي"
])

# ----------------------------
# تحليل الدومين
# ----------------------------
with tabs[0]:
    domain = st.text_input("أدخل اسم الدومين")
    if st.button("تحليل الدومين"):
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
    url = st.text_input("أدخل رابط الموقع")
    if st.button("فحص الموقع"):
        tech = website_scan.detect_tech(url)
        headers = website_scan.header_analysis(url)
        emails = website_scan.extract_emails(url)

        st.write("التقنيات المكتشفة", tech)
        st.write("الهيدرز", headers)
        st.write("الإيميلات المكتشفة", emails)

        st.session_state["scan"] = {
            "tech": tech,
            "headers": headers,
            "emails": emails
        }

# ----------------------------
# بحث عن المستخدم
# ----------------------------
with tabs[2]:

    st.header("🔍 البحث عن اسم مستخدم")

    username = st.text_input("أدخل اسم المستخدم")

    if st.button("بحث"):
        res = username_osint.username_search(username)

        if isinstance(res, dict) and res:
            st.success("تم العثور على الحسابات التالية:")
            for platform, link in res.items():
                st.write(f"✅ {platform} : {link}")
        else:
            st.warning("لم يتم العثور على حسابات بهذا الاسم")

# ----------------------------
# تحديد الموقع الجغرافي
# ----------------------------
with tabs[3]:
    ip = st.text_input("أدخل IP")

    if st.button("تحديد الموقع"):
        data = geoip_osint.geoip(ip)
        st.write(data)

# ----------------------------
# سطح الهجوم
# ----------------------------
with tabs[4]:
    if "subs" in st.session_state:

        file = attack_surface.draw_graph(
            st.session_state["domain"],
            st.session_state["subs"]
        )

        st.image(file)

    else:
        st.warning("قم أولاً بفحص النطاقات الفرعية")

# ----------------------------
# التحليل الذكي
# ----------------------------
with tabs[5]:

    if "subs" in st.session_state:

        analysis = ai_analysis.analyze_ports(
            st.session_state["domain"],
            list(st.session_state["subs"].values())
        )

        st.text(analysis)

    else:
        st.warning("قم أولاً بفحص النطاقات الفرعية")

# ----------------------------
# التقارير
# ----------------------------
with tabs[6]:

    if st.button("إنشاء تقرير PDF"):

        file = report_generator.create_report(st.session_state)

        with open(file, "rb") as f:
            st.download_button("تحميل التقرير", f, file_name=file)

# ----------------------------
# مساعد الهجوم الذكي
# ----------------------------
with tabs[7]:

    target = st.text_input("🎯 أدخل الدومين أو IP للتحليل")

    open_ports_input = st.text_input("المنافذ المفتوحة (مثال: 22,80,443)")
    tech_input = st.text_input("التقنيات المكتشفة (مثال: WordPress, Django)")

    if st.button("تحليل الهدف بالذكاء الاصطناعي"):

        open_ports = [
            int(p.strip())
            for p in open_ports_input.split(",")
            if p.strip().isdigit()
        ]

        tech_list = [
            t.strip()
            for t in tech_input.split(",")
            if t.strip()
        ]

        analysis = ai_hacking.analyze_target(
            target,
            open_ports,
            tech_list,
            headers=None
        )

        st.code(analysis)
