import os
import config
from tavily import TavilyClient

def darkweb_lookup(query):
    """
    البحث عن تسريبات في الشبكة المظلمة بأسلوب مستقر ومختصر.
    """
    tavily_api_key = config.get_key("TAVILY_API_KEY")
    if not tavily_api_key:
        return {"error": "⚠️ TAVILY_API_KEY غير موجود."}

    try:
        tavily = TavilyClient(api_key=tavily_api_key)
        search_query = f"dark web leaks and mentions of {query} summary"
        response = tavily.search(query=search_query, search_depth="basic")
        
        results = []
        if response and response.get("results"):
            for res in response["results"][:5]:
                results.append({
                    "title": res["title"],
                    "url": res["url"],
                    "snippet": res["content"][:250] + "..."
                })
        
        if not results:
            return {"message": f"لم يتم العثور على تسريبات معروفة لـ {query}."}

        return results
    except Exception as e:
        return {"error": f"⚠️ واجه النظام مشكلة أثناء البحث في الشبكة المظلمة."}
