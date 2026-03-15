import requests
from bs4 import BeautifulSoup
import re


# كشف التقنيات
def detect_tech(url):

    tech = []

    try:

        headers = {"User-Agent": "Mozilla/5.0"}

        r = requests.get(url, headers=headers, timeout=10)

        html = r.text.lower()

        if "wp-content" in html:
            tech.append("WordPress")

        if "react" in html:
            tech.append("React")

        if "vue" in html:
            tech.append("Vue")

        if "bootstrap" in html:
            tech.append("Bootstrap")

        if "jquery" in html:
            tech.append("jQuery")

        if "google-analytics" in html or "gtag(" in html:
            tech.append("Google Analytics")

        if "cloudflare" in str(r.headers).lower():
            tech.append("Cloudflare")

        if not tech:
            tech.append("لم يتم اكتشاف تقنيات")

        return tech

    except Exception as e:
        return [str(e)]


# تحليل الهيدرز
def header_analysis(url):

    try:

        r = requests.get(url, timeout=10)

        return dict(r.headers)

    except Exception as e:
        return {"error": str(e)}


# استخراج الايميلات
def extract_emails(url):

    try:

        r = requests.get(url, timeout=10)

        emails = re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            r.text
        )

        return list(set(emails))

    except Exception as e:
        return {"error": str(e)}
