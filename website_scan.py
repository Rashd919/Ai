import requests
import re

def detect_tech(url):
    """كشف التقنيات المستخدمة في الموقع"""
    tech = []
    try:
        r = requests.get(url, timeout=5)
        txt = r.text.lower()
        if "wordpress" in txt:
            tech.append("WordPress")
        if "react" in txt:
            tech.append("React")
        if "django" in txt:
            tech.append("Django")
        if "jquery" in txt:
            tech.append("jQuery")
    except:
        pass
    return tech

def header_analysis(url):
    """تحليل الهيدرز الأمنية"""
    try:
        r = requests.get(url, timeout=5)
        h = r.headers
        needed = [
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Strict-Transport-Security",
            "Referrer-Policy",
            "Permissions-Policy"
        ]
        return {k: h.get(k, "Missing") for k in needed}
    except:
        return {}

def extract_emails(url):
    """استخراج الإيميلات من صفحة الموقع"""
    try:
        r = requests.get(url, timeout=5)
        emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", r.text)
        return list(set(emails))
    except:
        return []
