import os
import config
from tavily import TavilyClient
from groq import Groq

def phone_lookup(number):
    """
    البحث عن معلومات رقم الهاتف وتحليلها بالذكاء الاصطناعي لتقديم نتيجة عربية نظيفة.
    """
    tavily_key = config.get_key("TAVILY_API_KEY")
    groq_key = config.get_key("GROQ_API_KEY")
    
    if not tavily_key:
        return "⚠️ مفتاح TAVILY_API_KEY غير موجود للبحث."

    try:
        # 1. البحث عن الرقم عبر Tavily
        tavily = TavilyClient(api_key=tavily_key)
        query = f'owner name and location for phone number {number} caller id info'
        response = tavily.search(query=query, search_depth="advanced")
        
        results = response.get("results", [])
        if not results:
            return f"❌ لم يتم العثور على معلومات عامة لرقم الهاتف: {number}"

        # 2. تحليل النتائج بالذكاء الاصطناعي (Groq) إذا توفر المفتاح
        if groq_key:
            client = Groq(api_key=groq_key)
            context = "\n".join([f"- {r['title']}: {r['content'][:300]}" for r in results[:5]])
            
            prompt = f"""
            أنت خبير استخبارات أمنية (OSINT). لديك نتائج بحث عن رقم الهاتف: {number}
            النتائج الخام:
            {context}
            
            المطلوب:
            قم بتحليل هذه النتائج واستخراج (الاسم المحتمل، الموقع، مزود الخدمة) إن وجد.
            قدم الإجابة باللغة العربية فقط، بشكل مختصر ومباشر جداً.
            إذا لم تجد اسماً صريحاً، قل "لم يتم العثور على اسم صريح، ولكن الرقم مرتبط بـ...".
            لا تظهر أي رموز برمجية أو أقواس أو JSON.
            """
            
            completion = client.chat.completions.create(
                model=config.GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}]
            )
            return completion.choices[0].message.content
        else:
            # عرض النتائج بشكل نصي بسيط إذا لم يتوفر Groq
            output = f"🔍 نتائج البحث عن الرقم {number}:\n\n"
            for r in results[:3]:
                output += f"🔹 {r['title']}\n🔗 {r['url']}\n\n"
            return output

    except Exception as e:
        return f"⚠️ خطأ أثناء البحث عن الهاتف: {str(e)}"
