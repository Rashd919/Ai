import os
import config
from tavily import TavilyClient

def search_dork(query):
    """
    بحث Google Dork متقدم باستخدام Tavily API.
    """
    tavily_api_key = config.get_key("TAVILY_API_KEY")
    if not tavily_api_key:
        return {"error": "⚠️ TAVILY_API_KEY غير موجود. يرجى إضافته في إعدادات Streamlit أو ملف .env"}

    try:
        tavily = TavilyClient(api_key=tavily_api_key)
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
            return {"message": f"لم يتم العثور على نتائج لـ {query}."}

        return results
    except Exception as e:
        return {"error": f"❌ خطأ في بحث Google Dork باستخدام Tavily: {str(e)}"}
