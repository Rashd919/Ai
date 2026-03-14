# geoip_osint.py
# وحدة تحليل الـ IP والموقع الجغرافي

import requests

def geoip(ip):
    """جلب معلومات الموقع الجغرافي عن IP"""
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?lang=ar", timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == "success":
                return {
                    "IP": ip,
                    "الدولة": data.get("country"),
                    "المدينة": data.get("city"),
                    "المزود": data.get("isp"),
                    "الخطوط الطول والعرض": f"{data.get('lat')}, {data.get('lon')}"
                }
            else:
                return {"خطأ": "تعذر تحديد الموقع"}
    except Exception as e:
        return {"خطأ": str(e)}
