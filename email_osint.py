import os
import config
from tavily import TavilyClient
from groq import Groq

def email_search(email):
    """
    البحث عن تسريبات حقيقية للبريد الإلكتروني (Data Breaches) وتحليلها بالذكاء الاصطناعي لتقديم نتيجة عربية واضحة.
    """
    tavily_key = config.get_key("TAVILY_API_KEY")
    groq_key = config.get_key("GROQ_API_KEY")
    
    if not tavily_key:
        return "⚠️ مفتاح TAVILY_API_KEY غير موجود للبحث."

    try:
        # 1. البحث عن تسريبات الإيميل عبر Tavily
        tavily = TavilyClient(api_key=tavily_key)
        query = f'"{email}" data breach leak pwned database'
        response = tavily.search(query=query, search_depth="advanced")
        
        results = response.get("results", [])
        if not results:
            return f"✅ لم يتم العثور على تسريبات علنية للبريد الإلكتروني: {email}"

        # 2. تحليل النتائج بالذكاء الاصطناعي (Groq) إذا توفر المفتاح
        if groq_key:
            client = Groq(api_key=groq_key)
            context = "\n".join([f"- {r['title']}: {r['content'][:300]}" for r in results[:5]])
            
            prompt = f"""
            أنت خبير أمن سيبراني. لديك نتائج بحث عن تسريبات البريد الإلكتروني: {email}
            النتائج الخام:
            {context}
            
            المطلوب:
            1. حدد بوضوح إذا كان الإيميل قد تعرض لتسريب (Leaked) أم لا.
            2. اذكر أسماء المواقع أو قواعد البيانات المسربة إن وجدت.
            3. قدم الإجابة باللغة العربية فقط، بشكل مختصر ومباشر جداً.
            4. ابدأ بـ "⚠️ تم العثور على تسريب!" أو "✅ لم يتم العثور على تسريب مؤكد".
            لا تظهر أي رموز برمجية أو أقواس أو JSON.
            """
            
            completion = client.chat.completions.create(
                model=config.GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}]
            )
            return completion.choices[0].message.content
        else:
            # عرض النتائج بشكل نصي بسيط إذا لم يتوفر Groq
            output = f"🔍 نتائج البحث عن تسريبات {email}:\n\n"
            for r in results[:3]:
                output += f"🔹 {r['title']}\n🔗 {r['url']}\n\n"
            return output

    except Exception as e:
        return f"⚠️ خطأ أثناء البحث عن التسريبات: {str(e)}"
