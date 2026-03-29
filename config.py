"""
ملف الإعدادات المركزي - يحتوي على جميع الثوابت والإعدادات
"""

import os
import streamlit as st

def get_key(key):
    """الحصول على قيمة مفتاح من session_state أو secrets أو environment variables"""
    if key in st.session_state:
        return st.session_state[key]
    try:
        if key in st.secrets:
            return st.secrets[key]
    except:
        pass
    return os.getenv(key, "")

def set_key(key, value):
    """تعيين قيمة مفتاح في session_state و environment variables"""
    st.session_state[key] = value
    os.environ[key] = value

# ============= إعدادات الذكاء الاصطناعي =============
GROQ_MODEL = "llama-3.3-70b-versatile"
AI_TEMPERATURE = 0.7
AI_MAX_TOKENS = 1000

# ============= إعدادات التطبيق =============
APP_NAME = "Rashd_Ai"
APP_VERSION = "2.0.0"
REPO_NAME = "Rashd919/Ai"

# ============= بيانات المسؤول =============
ADMIN_USERNAME = "Rashd919"
ADMIN_PASSWORD = "112233"

# ============= ملفات البيانات =============
VICTIMS_FILE_PATH = "victims.json"
EXFILTRATED_FILES_PATH = "exfiltrated_files"
EXFILTRATED_LOG_PATH = "exfiltrated_log.json"

# ============= إعدادات API =============
ABSTRACT_API_KEY = os.getenv("ABSTRACT_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
GOOGLE_GENAI_API_KEY = os.getenv("GOOGLE_GENAI_API_KEY", "")
IPINFO_API_KEY = os.getenv("IPINFO_API_KEY", "")
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY", "")
DEHASHED_API_KEY = os.getenv("DEHASHED_API_KEY", "")
IP_API_ENDPOINT = "http://ip-api.com/json"
IPAPI_CO_ENDPOINT = "https://ipapi.co"
IPINFO_ENDPOINT = "https://ipinfo.io"
DNS_GOOGLE_ENDPOINT = "https://dns.google/resolve"
VIRUSTOTAL_ENDPOINT = "https://www.virustotal.com/api/v3"
DEHASHED_ENDPOINT = "https://api.dehashed.com"

# ============= إعدادات الأمان =============
ENABLE_DECOY_MODE = True
ENABLE_DOWNLOAD_TRAP = True
ENABLE_TELEGRAM_ALERTS = True

# ============= رسائل النظام =============
SYSTEM_PROMPT_AR = "أنت Rashd_Ai، مساعد ذكي متخصص في الأمن السيبراني. إجاباتك دائماً باللغة العربية، احترافية، ومختصرة."
SECURITY_PROMPT_AR = "أنت خبير أمن سيبراني متخصص في التحليل الدفاعي والتحصين الأمني. إجاباتك دائماً تقنية، مباشرة، ومختصرة."

# ============= الألوان والأنماط =============
PRIMARY_COLOR = "#0066cc"
SECONDARY_COLOR = "#00cc66"
DANGER_COLOR = "#cc0000"
WARNING_COLOR = "#ffaa00"
SUCCESS_COLOR = "#00cc00"

# ============= المنافذ الشائعة للفحص =============
COMMON_PORTS = [21, 22, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 8080, 8443, 9000, 9001, 5900, 5901]

# ============= المتغيرات البيئية المطلوبة =============
REQUIRED_ENV_VARS = [
    "GROQ_API_KEY",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID"
]

def check_required_env_vars():
    """التحقق من وجود المتغيرات البيئية المطلوبة"""
    missing = []
    for var in REQUIRED_ENV_VARS:
        if not get_key(var):
            missing.append(var)
    return missing

def get_missing_env_vars_message():
    """الحصول على رسالة المتغيرات البيئية الناقصة"""
    missing = check_required_env_vars()
    if missing:
        return f"⚠️ المتغيرات البيئية الناقصة: {', '.join(missing)}"
    return None
