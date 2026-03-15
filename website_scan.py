import requests
from bs4 import BeautifulSoup

# -----------------------------
# كشف التقنيات المستخدمة
# -----------------------------
def detect_tech(url):

    tech = []

    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(url, headers=headers, timeout=10)

        html = r.text.lower()

        # كشف WordPress
        if "wp-content" in html:
            tech.append("WordPress")

        # كشف React
        if "react" in html:
            tech.append("React")

        # كشف Vue
        if "vue" in html:
            tech.append("Vue.js")

        # كشف Bootstrap
        if "bootstrap" in html:
            tech.append("Bootstrap")

        # كشف jQuery
        if "jquery" in html:
            tech.append("jQuery")

        # كشف Google Analytics
        if "google-analytics" in html or "gtag" in html:
            tech.append("Google Analytics")

        # كشف Cloudflare
        if "cloudflare" in str(r.headers).lower():
            tech.append("Cloudflare")

        if not tech:
            tech.append("لم يتم اكتشاف تقنيات واضحة")

        return tech

    except Exception as e:

        return [str(e)]


# -----------------------------
# تحليل Headers
# -----------------------------
def header_analysis(url):

    try:

        r = requests.get(url, timeout=10)

        return dict(r.headers)

    except Exception as e:

        return {"error": str(e)}


# -----------------------------
# استخراج الإيميلات
# -----------------------------
def extract_emails(url):

    import re

    try:

        r = requests.get(url, timeout=10)

        emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", r.text)

        return list(set(emails))

    except Exception as e:

        return {"error": str(e)}
