# website_scan.py
import requests
from bs4 import BeautifulSoup

def detect_tech(url):
    """كشف تقنيات الموقع"""
    tech = []
    try:
        r = requests.get(url, timeout=5)
        headers = r.headers
        if "X-Powered-By" in headers:
            tech.append(headers["X-Powered-By"])
        if "Server" in headers:
            tech.append(headers["Server"])
        html = r.text.lower()
        if "wp-content" in html:
            tech.append("WordPress")
        if "django" in html:
            tech.append("Django")
        return tech
    except:
        return []

def header_analysis(url):
    """تحليل الهيدرز"""
    try:
        r = requests.get(url, timeout=5)
        return dict(r.headers)
    except:
        return {}

def extract_emails(url):
    """استخراج الإيميلات من الموقع"""
    emails = set()
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text()
        import re
        for e in re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}", text):
            emails.add(e)
        return list(emails)
    except:
        return []
