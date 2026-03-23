import requests
import json
import config

def get_ip_geolocation(ip_addresses):
    """
    يسترجع معلومات الموقع الجغرافي لعناوين IP باستخدام IP-API.com Batch API.
    يدعم اللغة العربية (locale=ar) ويستخدم مفتاح API إذا توفر.
    """
    if not isinstance(ip_addresses, list):
        ip_addresses = [ip_addresses]

    api_key = config.IP_API_KEY
    base_url = "http://ip-api.com/batch"
    params = {"lang": "ar"}

    if api_key:
        base_url = "https://pro.ip-api.com/batch"
        params["key"] = api_key

    try:
        response = requests.post(base_url, json=ip_addresses, params=params)
        response.raise_for_status()  # يرفع استثناء لأخطاء HTTP
        data = response.json()

        results = []
        for item in data:
            if item and item.get("status") == "success":
                result = {
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
                }
                results.append(result)
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
