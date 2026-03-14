# geoip_osint.py
import requests

def geoip(ip):
    """تحديد الموقع الجغرافي لعنوان IP"""
    try:
        r = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
        if r.status_code == 200:
            data = r.json()
            result = {
                "IP": data.get("ip"),
                "الدولة": data.get("country_name"),
                "المدينة": data.get("city"),
                "المنطقة/المقاطعة": data.get("region"),
                "الرمز البريدي": data.get("postal"),
                "خط الطول": data.get("latitude"),
                "خط العرض": data.get("longitude"),
                "مزود الخدمة": data.get("org")
            }
            return result
        return {"خطأ": "تعذر الحصول على بيانات الموقع"}
    except Exception as e:
        return {"خطأ": str(e)}
