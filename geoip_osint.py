import requests

def geoip(ip):
    """
    جلب معلومات الموقع الجغرافي للـ IP
    """
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)

        if r.status_code == 200:
            data = r.json()

            return {
                "IP": data.get("query"),
                "Country": data.get("country"),
                "Region": data.get("regionName"),
                "City": data.get("city"),
                "ISP": data.get("isp"),
                "Org": data.get("org"),
                "Latitude": data.get("lat"),
                "Longitude": data.get("lon")
            }

    except Exception as e:
        return {"error": str(e)}

    return {}
