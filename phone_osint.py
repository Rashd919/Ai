import os
import config
from tavily import TavilyClient
from groq import Groq

def phone_lookup(number):
    """
    البحث العميق عن رقم الهاتف في منصات التواصل الاجتماعي وقواعد البيانات المفتوحة وتحليلها بالذكاء الاصطناعي.
    """
    tavily_key = config.get_key("TAVILY_API_KEY")
    groq_key = config.get_key("GROQ_API_KEY")
    
    if not tavily_key:
        return "⚠️ مفتاح TAVILY_API_KEY غير موجود للبحث."

    try:
        # 1. البحث العميق عبر Tavily (لإيجاد الاسم والحسابات المرتبطة)
        tavily = TavilyClient(api_key=tavily_key)
        # استعلامات بحث متعددة لضمان أفضل النتائج
        queries = [
            f'owner name and social media profiles for phone number "{number}"',
            f'"{number}" facebook instagram tiktok twitter linkedin profile',
            f'"{number}" caller id info location service provider'
        ]
        
        all_results = []
        for q in queries:
            response = tavily.search(query=q, search_depth="advanced")
            all_results.extend(response.get("results", []))
        
        if not all_results:
            return f"❌ لم يتم العثور على معلومات علنية مرتبطة برقم الهاتف: {number}"

        # 2. تحليل النتائج بالذكاء الاصطناعي (Groq) لتقديم عرض نظيف وحقيقي
        if groq_key:
            client = Groq(api_key=groq_key)
            # تجميع محتوى فريد من النتائج
            unique_content = []
            seen_urls = set()
            for r in all_results:
                if r['url'] not in seen_urls:
                    unique_content.append(f"- {r['title']}: {r['content'][:300]}")
                    seen_urls.add(r['url'])
            
            context = "\n".join(unique_content[:10])
            
            prompt = f"""
            أنت خبير استخبارات أمنية (OSINT). لديك نتائج بحث عن رقم الهاتف: {number}
            النتائج الخام:
            {context}
            
            المطلوب:
            1. استخرج (الاسم الحقيقي أو المحتمل، الموقع الجغرافي، مزود الخدمة).
            2. ابحث عن أي روابط لملفات شخصية على (فيسبوك، إنستغرام، تيك توك، واتساب، إلخ) مرتبطة بهذا الرقم.
            3. قدم الإجابة باللغة العربية فقط، بشكل مرتب، مختصر، ومباشر جداً.
            4. لا تظهر أي رموز برمجية أو JSON أو أقواس.
            5. ابدأ بـ "🔍 نتائج التحقيق للرقم {number}:"
            """
            
            completion = client.chat.completions.create(
                model=config.GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}]
            )
            return completion.choices[0].message.content
        else:
            # عرض النتائج بشكل نصي بسيط إذا لم يتوفر Groq
            output = f"🔍 نتائج البحث عن الرقم {number}:\n\n"
            seen_urls = set()
            for r in all_results:
                if r['url'] not in seen_urls:
                    output += f"🔹 {r['title']}\n🔗 {r['url']}\n\n"
                    seen_urls.add(r['url'])
                    if len(seen_urls) >= 5: break
            return output

    except Exception as e:
        return f"⚠️ خطأ أثناء البحث عن الهاتف: {str(e)}"
