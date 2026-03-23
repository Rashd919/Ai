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
    params = {"lang": "ar"}

    if api_key:
        # استخدام النسخة الاحترافية إذا توفر مفتاح API
        base_url_single = "https://pro.ip-api.com/json/"
        base_url_batch = "https://pro.ip-api.com/batch"
        params["key"] = api_key
    else:
        # استخدام النسخة المجانية
        base_url_single = "http://ip-api.com/json/"
        base_url_batch = "http://ip-api.com/batch"

    results = []
    try:
        if len(cleaned_ip_addresses) == 1:
            # طلب فردي لعنوان IP واحد
            ip = cleaned_ip_addresses[0]
            response = requests.get(f"{base_url_single}{ip}", params=params)
            response.raise_for_status()
            data = response.json()
            if data and data.get("status") == "success":
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
            elif data and data.get("status") == "fail":
                results.append({"error": data.get("message", "فشل في جلب معلومات IP.")})
            else:
                results.append({"error": "استجابة غير متوقعة من IP-API.com"})
        else:
            # طلب جماعي لعدة عناوين IP
            response = requests.post(base_url_batch, json=cleaned_ip_addresses, params=params)
            response.raise_for_status()
            data = response.json()
            for item in data:
                if item and item.get("status") == "success":
                    results.append({
                        "عنوان IP": item.get("query"),
                        "الدولة": item.get("country"),
                        "رمز الدولة": item.get("countryCode"),
                        "المنطقة": item.get("regionName"),
                        "المدينة": item.get("city"),
                        "الرمز البريدي": item.get("zip"),
                        "خط العرض": item.get("lat"),
                        "خط الطول": item.get("lon"),
                        "المنطقة الزمنية": item.get("timezone"),
                        "مزود الخدمة": item.get("isp"),
                        "المنظمة": item.get("org"),
                        "AS": item.get("as"),
                    })
                elif item and item.get("status") == "fail":
                    results.append({"error": item.get("message", "فشل في جلب معلومات IP.")})
                else:
                    results.append({"error": "استجابة غير متوقعة من IP-API.com"})
        return results
    except requests.exceptions.RequestException as e:
        return [{"error": f"خطأ في الاتصال بـ IP-API.com: {e}"}]
    except json.JSONDecodeError:
        return [{"error": "فشل في تحليل استجابة JSON من IP-API.com"}]
    except Exception as e:
        return [{"error": f"حدث خطأ غير متوقع: {e}"}]
