import os
from tavily import TavilyClient
import config

def scan_vulnerabilities(target):
    """
    البحث عن الثغرات الأمنية بأسلوب مستقر ومختصر.
    """
    tavily_api_key = config.get_key("TAVILY_API_KEY")
    if not tavily_api_key:
        return {"error": "⚠️ TAVILY_API_KEY غير موجود."}

    try:
        tavily = TavilyClient(api_key=tavily_api_key)
        query = f"known CVE and security vulnerabilities for {target} summary"
        response = tavily.search(query=query, search_depth="basic")
        
        results = []
        if response and response.get("results"):
            for res in response["results"][:5]: # نأخذ أهم 5 نتائج
                results.append({
                    "title": res["title"],
                    "url": res["url"],
                    "snippet": res["content"][:250] + "..."
                })
        
        if not results:
            return {"message": f"لم يتم العثور على ثغرات معروفة لـ {target}."}

        return results
    except Exception as e:
        # في حال فشل Tavily، نحاول إرجاع رسالة مفهومة بدلاً من الخطأ التقني
        return {"error": f"⚠️ واجه النظام مشكلة أثناء الفحص. يرجى المحاولة لاحقاً."}
