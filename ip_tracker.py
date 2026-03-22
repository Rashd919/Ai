import requests
import json

def get_ip_geolocation(ip_address):
    """
    يسترجع معلومات الموقع الجغرافي لعنوان IP باستخدام IP-API.com.
    """
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        response.raise_for_status()  # يرفع استثناء لأخطاء HTTP
        data = response.json()
        
        if data and data.get("status") == "success":
            # تنسيق النتائج لعرضها بشكل واضح
            result = {
                "IP Address": data.get("query"),
                "Country": data.get("country"),
                "Country Code": data.get("countryCode"),
                "Region": data.get("regionName"),
                "City": data.get("city"),
                "Zip Code": data.get("zip"),
                "Latitude": data.get("lat"),
                "Longitude": data.get("lon"),
                "Timezone": data.get("timezone"),
                "ISP": data.get("isp"),
                "Organization": data.get("org"),
                "AS": data.get("as"),
            }
            return result
        elif data and data.get("status") == "fail":
            return {"error": data.get("message", "فشل في جلب معلومات IP.")}
        else:
            return {"error": "استجابة غير متوقعة من IP-API.com"}
    except requests.exceptions.RequestException as e:
        return {"error": f"خطأ في الاتصال بـ IP-API.com: {e}"}
    except json.JSONDecodeError:
        return {"error": "فشل في تحليل استجابة JSON من IP-API.com"}
    except Exception as e:
        return {"error": f"حدث خطأ غير متوقع: {e}"}
