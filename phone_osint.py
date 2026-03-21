import os
import config
from tavily import TavilyClient

def phone_lookup(number):
    """
    البحث عن معلومات حول رقم الهاتف باستخدام Tavily API بأسلوب مختصر.
    """
    tavily_api_key = config.get_key("TAVILY_API_KEY")
    if not tavily_api_key:
        return {"error": "⚠️ TAVILY_API_KEY غير موجود."}

    try:
        tavily = TavilyClient(api_key=tavily_api_key)
        # البحث عن معلومات محددة ومختصرة
        query = f"owner name and location for phone number {number} summary"
        response = tavily.search(query=query, search_depth="basic") # استخدام basic لنتائج أسرع وأقل تشتيتاً
        
        results = []
        if response and response.get("results"):
            # نأخذ أول 3 نتائج فقط لضمان الاختصار
            for res in response["results"][:3]:
                results.append({
                    "title": res["title"],
                    "url": res["url"],
                    "snippet": res["content"][:200] + "..." # اختصار النص
                })
        
        if not results:
            return {"message": f"لم يتم العثور على معلومات واضحة لـ {number}."}

        return results
    except Exception as e:
        return {"error": f"❌ خطأ في البحث: {str(e)}"}
