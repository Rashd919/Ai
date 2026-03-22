import requests
import config
from groq import Groq
from tavily import TavilyClient

PLATFORMS = {
    "Facebook": "https://www.facebook.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "Twitter/X": "https://twitter.com/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "LinkedIn": "https://www.linkedin.com/in/{}",
    "GitHub": "https://github.com/{}",
    "Pinterest": "https://www.pinterest.com/{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "YouTube": "https://www.youtube.com/@{}"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

def username_search(username):
    """
    البحث العميق عن اسم المستخدم في منصات التواصل الاجتماعي وتحليل النتائج بالذكاء الاصطناعي.
    """
    groq_key = config.get_key("GROQ_API_KEY")
    tavily_key = config.get_key("TAVILY_API_KEY")
    
    found_profiles = []
    
    # 1. فحص الروابط المباشرة (Fast Check)
    for platform, url_template in PLATFORMS.items():
        full_url = url_template.format(username)
        try:
            # محاولة التحقق من وجود الحساب (بعض المنصات تمنع هذا الفحص المباشر)
            r = requests.get(full_url, headers=HEADERS, timeout=3, allow_redirects=True)
            if r.status_code == 200 and "login" not in r.url.lower() and "404" not in r.text:
                found_profiles.append(f"✅ {platform}: {full_url}")
        except:
            continue

    # 2. البحث العميق عبر Tavily (لإيجاد حسابات إضافية)
    if tavily_key:
        try:
            tavily = TavilyClient(api_key=tavily_key)
            search_query = f'"{username}" social media profiles facebook instagram tiktok twitter linkedin'
            response = tavily.search(query=search_query, search_depth="advanced")
            for res in response.get("results", []):
                found_profiles.append(f"🔗 {res['title']}: {res['url']}")
        except:
            pass

    if not found_profiles:
        return f"❌ لم يتم العثور على حسابات علنية مرتبطة باسم المستخدم: {username}"

    # 3. تحليل النتائج بالذكاء الاصطناعي (Groq) لتقديم عرض نظيف
    if groq_key:
        try:
            client = Groq(api_key=groq_key)
            context = "\n".join(found_profiles[:15])
            
            prompt = f"""
            أنت خبير استخبارات أمنية (OSINT). لديك قائمة بحسابات تواصل اجتماعي محتملة لاسم المستخدم: {username}
            القائمة:
            {context}
            
            المطلوب:
            1. قم بتنظيم هذه الحسابات في قائمة عربية واضحة ومرتبة.
            2. تأكد من ذكر اسم المنصة والرابط بجانبها.
            3. إذا وجدت معلومات إضافية (مثل الاسم الحقيقي أو الوصف)، اذكرها باختصار.
            4. لا تظهر أي رموز برمجية أو JSON أو أقواس.
            5. ابدأ بـ "🔍 تم العثور على الحسابات التالية لـ {username}:"
            """
            
            completion = client.chat.completions.create(
                model=config.GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}]
            )
            return completion.choices[0].message.content
        except Exception as e:
            return "\n".join(found_profiles)
    
    return "\n".join(found_profiles)
