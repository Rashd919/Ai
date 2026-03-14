# website_scan.py
# وحدة فحص المواقع واستخراج المعلومات التقنية

import requests
import re
from bs4 import BeautifulSoup

def detect_tech(url):
    """كشف التقنيات المستخدمة في الموقع"""
    tech = []
    try:
        r = requests.get(url, timeout=5)
        headers, txt = r.headers, r.text.lower()
        if "x-powered-by" in headers:
            tech.append(headers["x-powered-by"])
        if "x-generator" in headers:
            tech.append(headers["x-generator"])
        if "wordpress" in txt:
            tech.append("WordPress")
        if "django" in txt:
            tech.append("Django")
        if "react" in txt or "next.js" in txt:
            tech.append("React/Next")
        if "jquery" in txt:
            tech.append("jQuery")
    except:
        pass
    return list(set(tech))

def header_analysis(url):
    """تحليل الهيدرز الأساسية للموقع"""
    try:
        r = requests.get(url, timeout=5)
        headers = r.headers
        needed = ["Content-Security-Policy","X-Frame-Options","X-Content-Type-Options",
                  "Strict-Transport-Security","Referrer-Policy","Permissions-Policy"]
        return {k: headers.get(k, "غير موجود") for k in needed}
    except Exception as e:
        return {"خطأ": str(e)}

def extract_emails(url):
    """استخراج البريد الإلكتروني من صفحات الموقع"""
    try:
        r = requests.get(url, timeout=5)
        emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", r.text)
        return list(set(emails))
    except Exception as e:
        return {"خطأ": str(e)}
