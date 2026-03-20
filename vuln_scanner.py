import os
from tavily import TavilyClient
import config

def scan_vulnerabilities(target):
    """
    البحث عن الثغرات الأمنية للهدف باستخدام Tavily API.
    """
    tavily_api_key = config.get_key("TAVILY_API_KEY")
    if not tavily_api_key:
        return {"error": "⚠️ TAVILY_API_KEY غير موجود. يرجى إضافته في إعدادات Streamlit أو ملف .env"}

    try:
        tavily = TavilyClient(api_key=tavily_api_key)
        # البحث عن ثغرات معروفة للهدف
        query = f"known vulnerabilities and CVE for {target}"
        response = tavily.search(query=query, search_depth="advanced")
        
        results = []
        if response and response.get("results"):
            for res in response["results"]:
                results.append({
                    "title": res["title"],
                    "url": res["url"],
                    "snippet": res["content"]
                })
        
        if not results:
            return {"message": f"لم يتم العثور على ثغرات معروفة لـ {target}."}

        return results
    except Exception as e:
        return {"error": f"❌ خطأ في فحص الثغرات باستخدام Tavily: {str(e)}"}
