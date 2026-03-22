import requests
import config

def send_telegram_message(message):
    """
    إرسال رسالة إلى تلجرام باستخدام Bot API.
    """
    token = config.get_key("TELEGRAM_BOT_TOKEN")
    chat_id = config.get_key("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        return False, "⚠️ إعدادات تلجرام غير مكتملة (Token أو Chat ID مفقود)."

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            return True, "✅ تم إرسال التنبيه إلى تلجرام بنجاح."
        else:
            return False, f"❌ فشل الإرسال: {response.json().get('description')}"
    except Exception as e:
        return False, f"❌ خطأ في الاتصال بتلجرام: {str(e)}"

def send_telegram_report(file_path):
    """
    إرسال ملف (مثل تقرير PDF) إلى تلجرام.
    """
    token = config.get_key("TELEGRAM_BOT_TOKEN")
    chat_id = config.get_key("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        return False, "⚠️ إعدادات تلجرام غير مكتملة."

    url = f"https://api.telegram.org/bot{token}/sendDocument"
    try:
        with open(file_path, "rb") as doc:
            files = {"document": doc}
            payload = {"chat_id": chat_id}
            response = requests.post(url, data=payload, files=files, timeout=30)
            if response.status_code == 200:
                return True, "✅ تم إرسال التقرير إلى تلجرام بنجاح."
            else:
                return False, f"❌ فشل إرسال الملف: {response.json().get('description')}"
    except Exception as e:
        return False, f"❌ خطأ في إرسال الملف: {str(e)}"
