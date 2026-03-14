import streamlit as st
from modules import domain_osint, website_scan, username_osint, geoip_osint, attack_surface, ai_analysis, report_generator

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
    "Reports"
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
