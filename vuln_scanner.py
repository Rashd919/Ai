import os
from tavily import TavilyClient

def scan_vulnerabilities(target):
    """
    البحث عن الثغرات الأمنية للهدف باستخدام Tavily API.
    """
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        return {"error": "TAVILY_API_KEY غير موجود في متغيرات البيئة"}

    tavily = TavilyClient(api_key=tavily_api_key)

    try:
        # البحث عن ثغرات معروفة للهدف
        query = f"known vulnerabilities for {target}"
        response = tavily.search(query=query, search_depth="advanced")
        
        results = []
        if response and response["results"]:
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
        return {"error": f"خطأ في فحص الثغرات باستخدام Tavily: {str(e)}"}
