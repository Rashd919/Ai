import os
import config
from tavily import TavilyClient
from groq import Groq

def email_search(email):
    """
    البحث عن تسريبات حقيقية للبريد الإلكتروني (Data Breaches) وتحليلها.
    """
    tavily_api_key = config.get_key("TAVILY_API_KEY")
    groq_api_key = config.get_key("GROQ_API_KEY")
    
    if not tavily_api_key:
        return {"error": "⚠️ TAVILY_API_KEY غير موجود."}

    try:
        tavily = TavilyClient(api_key=tavily_api_key)
        # البحث في قواعد بيانات التسريبات المعروفة والأخبار المتعلقة بها
        query = f'"{email}" data breach leak pwned database'
        response = tavily.search(query=query, search_depth="advanced")
        
        search_results = []
        if response and response.get("results"):
            for res in response["results"]:
                search_results.append({
                    "title": res["title"],
                    "url": res["url"],
                    "snippet": res["content"]
                })
        
        # تحليل النتائج بالذكاء الاصطناعي لإعطاء إجابة قاطعة
        analysis = "لم يتم العثور على تسريبات واضحة."
        if groq_api_key and search_results:
            client = Groq(api_key=groq_api_key)
            prompt = f"""
            بناءً على نتائج البحث التالية للإيميل ({email})، هل هذا الإيميل مسرب (Leaked) في أي قاعدة بيانات؟
            
            النتائج:
            {search_results[:5]}
            
            المطلوب:
            1. ابدأ بكلمة "⚠️ تم العثور على تسريب!" أو "✅ لم يتم العثور على تسريب مؤكد".
            2. اذكر أسماء المواقع أو قواعد البيانات المسربة إن وجدت.
            3. قدم نصيحة سريعة (مثل تغيير كلمة المرور).
            
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
        return {"error": f"❌ خطأ في فحص الإيميل: {str(e)}"}
