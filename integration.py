import os
import json
import asyncio
import telegram
from gtts import gTTS
from supabase import create_client, Client
from datetime import datetime
from dotenv import load_dotenv
import requests

load_dotenv()

# --- إعدادات Supabase ---
def get_supabase_client():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if url and key:
        return create_client(url, key)
    return None

def save_to_supabase(data, table_name="reports"):
    """حفظ البيانات في Supabase"""
    supabase = get_supabase_client()
    if not supabase:
        return "❌ إعدادات Supabase غير مكتملة."
    try:
        if "created_at" not in data:
            data["created_at"] = datetime.now().isoformat()
        response = supabase.table(table_name).insert(data).execute()
        return f"✅ تم الحفظ في Supabase: {response.data}"
    except Exception as e:
        return f"❌ خطأ Supabase: {str(e)}"

# --- إعدادات تلجرام ---
async def send_telegram_msg(text, include_voice=True):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return "❌ إعدادات تلجرام غير مكتملة."
    
    bot = telegram.Bot(token=token)
    try:
        # إرسال النص
        await bot.send_message(chat_id=chat_id, text=f"📋 **تقرير جديد من Ai Platform:**\n\n{text}")
        
        # إرسال الصوت
        if include_voice:
            voice_text = text[:500] # تحديد الطول للصوت
            tts = gTTS(text=voice_text, lang='ar')
            voice_file = "report_voice.mp3"
            tts.save(voice_file)
            with open(voice_file, 'rb') as audio:
                await bot.send_voice(chat_id=chat_id, voice=audio)
            os.remove(voice_file)
        return "✅ تم الإرسال لتلجرام بنجاح."
    except Exception as e:
        return f"❌ خطأ تلجرام: {str(e)}"

def send_report_to_telegram(text, include_voice=True):
    """دالة وسيطة لتشغيل التلجرام بشكل متزامن"""
    try:
        return asyncio.run(send_telegram_msg(text, include_voice))
    except Exception as e:
        try:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(send_telegram_msg(text, include_voice))
        except:
            return f"❌ فشل تشغيل التلجرام: {str(e)}"

# --- إعدادات Tavily ---
def tavily_search(query):
    """البحث باستخدام Tavily"""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "❌ مفتاح Tavily غير موجود."
    
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "advanced",
        "include_answer": True
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        return f"❌ خطأ Tavily: {str(e)}"
