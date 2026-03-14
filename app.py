import streamlit as st
import domain_osint
import website_scan
import username_osint
import geoip_osint
import attack_surface
import ai_analysis
import report_generator
from ai_hacking import ai_hacking   # <-- استيراد AI Hacking Assistant

st.set_page_config(page_title="CyberShield Pro OSINT", layout="wide")
st.title("🛡 CyberShield Pro OSINT Intelligence Platform")

# --- Tabs ---
tabs = st.tabs([
    "Domain OSINT",
    "Website Scan",
    "Username OSINT",
    "GeoIP",
    "Attack Surface",
    "AI Analysis",
    "Reports",
    "🤖 AI Hacking Assistant"   # <-- تبويب جديد
])

# ----------------------------
# Domain OSINT
# ----------------------------
with tabs[0]:
    domain = st.text_input("Domain")
    if st.button("Analyze Domain"):
        whois = domain_osint.whois_lookup(domain)
        dns = domain_osint.dns_lookup(domain)
        subs = domain_osint.subdomain_scan(domain)
        st.write("WHOIS", whois)
        st.write("DNS", dns)
        st.write("Subdomains", subs)
        st.session_state["domain"] = domain
        st.session_state["subs"] = subs

# ----------------------------
# Website Scan
# ----------------------------
with tabs[1]:
    url = st.text_input("Website URL")
    if st.button("Scan Website"):
        tech = website_scan.detect_tech(url)
        headers = website_scan.header_analysis(url)
        emails = website_scan.extract_emails(url)
        st.write("Tech", tech)
        st.write("Headers", headers)
        st.write("Emails", emails)
        st.session_state["scan"] = {"tech": tech, "headers": headers, "emails": emails}

# ----------------------------
# Username OSINT
# ----------------------------
with tabs[2]:
    username = st.text_input("Username")
    if st.button("Search Username"):
        result = username_osint.username_search(username)
        st.write(result)

# ----------------------------
# GeoIP Lookup
# ----------------------------
with tabs[3]:
    ip = st.text_input("IP")
    if st.button("Lookup IP"):
        data = geoip_osint.geoip(ip)
        st.write(data)

# ----------------------------
# Attack Surface
# ----------------------------
with tabs[4]:
    if "subs" in st.session_state:
        file = attack_surface.draw_graph(st.session_state["domain"], st.session_state["subs"])
        st.image(file)
    else:
        st.warning("Run subdomain scan first")

# ----------------------------
# AI Analysis
# ----------------------------
with tabs[5]:
    if "subs" in st.session_state:
        analysis = ai_analysis.analyze_ports(st.session_state["domain"], list(st.session_state["subs"].values()))
        st.write(analysis)
    else:
        st.warning("Run subdomain scan first")

# ----------------------------
# Reports
# ----------------------------
with tabs[6]:
    if st.button("Generate Report"):
        file = report_generator.create_report(st.session_state)
        with open(file, "rb") as f:
            st.download_button("Download Report", f, file_name=file)

# ----------------------------
# AI Hacking Assistant
# ----------------------------
with tabs[7]:
    target = st.text_input("🎯 Target Domain or IP for AI Hacking Analysis")
    open_ports_input = st.text_input("Open Ports (e.g., 22,80,443)")
    tech_input = st.text_input("Detected Technologies (e.g., WordPress, Django)")
    
    if st.button("Analyze Target with AI"):
        open_ports = [int(p.strip()) for p in open_ports_input.split(",") if p.strip().isdigit()]
        tech_list = [t.strip() for t in tech_input.split(",") if t.strip()]
        analysis = ai_hacking.analyze_target(target, open_ports, tech_list, headers=None)
        st.code(analysis)
