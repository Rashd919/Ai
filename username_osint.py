# username_osint.py
import requests

# قائمة المنصات والروابط
PLATFORMS = {
    "Pinterest": "https://www.pinterest.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "GitHub": "https://github.com/{}",
    "TikTok": "https://www.tiktok.com/@{}"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def username_search(username):
    """
    يبحث عن اسم المستخدم في المنصات المشهورة.
    يرجع فقط الروابط الموجودة فعلياً.
    """
    results = {}
    for platform, url in PLATFORMS.items():
        full_url = url.format(username)
        try:
            r = requests.get(full_url, headers=HEADERS, timeout=5)
            if r.status_code == 200:
                results[platform] = full_url
        except:
            continue
    return results
