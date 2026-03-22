import os
import config
from tavily import TavilyClient

def scan_ports(target):
    """
    البحث عن المنافذ المفتوحة الحقيقية المسجلة للهدف باستخدام Tavily API.
    """
    api_key = config.get_key("TAVILY_API_KEY")
    if not api_key:
        return "⚠️ TAVILY_API_KEY غير موجود لفحص المنافذ."

    try:
        tavily = TavilyClient(api_key=api_key)
        # البحث عن معلومات المنافذ المفتوحة للهدف
        query = f'open ports and services for {target} nmap scan results'
        response = tavily.search(query=query, search_depth="advanced")
        
        if response and response.get("results"):
            results_text = f"🔍 نتائج البحث عن المنافذ المفتوحة لـ {target}:\n\n"
            for res in response["results"]:
                results_text += f"🔹 **{res['title']}**\n"
                results_text += f"🔗 [المصدر]({res['url']})\n"
                results_text += f"📝 {res['content'][:300]}...\n\n"
            return results_text
        else:
            return f"❌ لم يتم العثور على معلومات عامة عن المنافذ المفتوحة لـ {target}."
    except Exception as e:
        return f"⚠️ خطأ أثناء فحص المنافذ: {str(e)}"
