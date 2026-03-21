import os
import config
from tavily import TavilyClient
from groq import Groq

def darkweb_lookup(query):
    """
    البحث عن تسريبات في أرشيفات الدارك ويب وقواعد بيانات التسريبات.
    """
    tavily_api_key = config.get_key("TAVILY_API_KEY")
    groq_api_key = config.get_key("GROQ_API_KEY")
    
    if not tavily_api_key:
        return {"error": "⚠️ TAVILY_API_KEY غير موجود."}

    try:
        tavily = TavilyClient(api_key=tavily_api_key)
        # البحث في المواقع التي تؤرشف بيانات الدارك ويب والتسريبات
        search_query = f'"{query}" site:pastebin.com OR site:ghostbin.com OR site:leaked.site OR "dark web leak" OR "onion link leak"'
        response = tavily.search(query=search_query, search_depth="advanced")
        
        search_results = []
        if response and response.get("results"):
            for res in response["results"]:
                search_results.append({
                    "title": res["title"],
                    "url": res["url"],
                    "snippet": res["content"]
                })
        
        # تحليل النتائج بالذكاء الاصطناعي
        analysis = "لم يتم العثور على نتائج في أرشيفات الدارك ويب."
        if groq_api_key and search_results:
            client = Groq(api_key=groq_api_key)
            prompt = f"""
            بناءً على نتائج البحث التالية للكلمة ({query})، هل هناك أي تسريبات منسوبة للدارك ويب (Dark Web)؟
            
            النتائج:
            {search_results[:5]}
            
            المطلوب:
            1. ابدأ بكلمة "🌑 تم العثور على نشاط في الدارك ويب!" أو "✅ لا يوجد نشاط مشبوه في الدارك ويب".
            2. اذكر نوع البيانات المسربة (إيميلات، كلمات مرور، بيانات بنكية) إن وجدت.
            3. قدم تحذيراً أمنياً.
            
            اجعل الإجابة باللغة العربية، مختصرة جداً، ومباشرة.
            """
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=config.GROQ_MODEL,
                temperature=0.3,
                max_tokens=500
            )
            analysis = chat_completion.choices[0].message.content

        return {
            "Analysis": analysis,
            "Results": search_results
        }
    except Exception as e:
        return {"error": f"⚠️ واجه النظام مشكلة أثناء البحث في الدارك ويب."}
