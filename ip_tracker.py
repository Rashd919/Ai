import requests
import json
import config

def get_ip_geolocation(ip_addresses):
    """
    يسترجع معلومات الموقع الجغرافي لعناوين IP باستخدام IP-API.com.
    يدعم اللغة العربية (locale=ar) ويستخدم مفتاح API إذا توفر.
    """
    if not isinstance(ip_addresses, list):
        ip_addresses = [ip_addresses]
    
    # تنظيف عناوين IP وإزالة المسافات الزائدة
    cleaned_ip_addresses = [ip.strip() for ip in ip_addresses if ip.strip()]

    if not cleaned_ip_addresses:
        return []

    api_key = config.IP_API_KEY
    results = []

    for ip in cleaned_ip_addresses:
        # محاولة الاتصال عبر HTTPS أولاً، ثم HTTP إذا فشل
        base_url_https = f"https://pro.ip-api.com/json/{ip}" if api_key else f"https://ip-api.com/json/{ip}"
        base_url_http = f"http://ip-api.com/json/{ip}"
        
        params = {"lang": "ar"}
        if api_key:
            params["key"] = api_key

        data = None
        try:
            # محاولة HTTPS
            response = requests.get(base_url_https, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
        except (requests.exceptions.RequestException, json.JSONDecodeError):
            # إذا فشل HTTPS، محاولة HTTP
            try:
                response = requests.get(base_url_http, params=params, timeout=5)
                response.raise_for_status()
                data = response.json()
            except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
                results.append({"error": f"فشل الاتصال بـ IP-API.com لـ {ip}: {e}"})
                continue
        
        if data:
            if data.get("status") == "success":
                results.append({
                    "عنوان IP": data.get("query"),
                    "الدولة": data.get("country"),
                    "رمز الدولة": data.get("countryCode"),
                    "المنطقة": data.get("regionName"),
                    "المدينة": data.get("city"),
                    "الرمز البريدي": data.get("zip"),
                    "خط العرض": data.get("lat"),
                    "خط الطول": data.get("lon"),
                    "المنطقة الزمنية": data.get("timezone"),
                    "مزود الخدمة": data.get("isp"),
                    "المنظمة": data.get("org"),
                    "AS": data.get("as"),
                })
            elif data.get("status") == "fail":
                results.append({"error": f"فشل جلب معلومات IP لـ {ip}: {data.get('message', 'خطأ غير معروف')}"})
            else:
                results.append({"error": f"استجابة غير متوقعة من IP-API.com لـ {ip}"})
        else:
            results.append({"error": f"لم يتم استلام بيانات من IP-API.com لـ {ip}"})

    return results
