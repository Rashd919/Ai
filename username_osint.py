# username_osint.py
import requests

PLATFORMS = {
    "Pinterest": "https://www.pinterest.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "GitHub": "https://github.com/{}",
    "TikTok": "https://www.tiktok.com/@{}"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ar,en;q=0.9",
}

def username_search(username):
    results = {}
    for platform, url in PLATFORMS.items():
        full_url = url.format(username)
        try:
            r = requests.get(full_url, headers=HEADERS, timeout=5, allow_redirects=True)
            # نتأكد من أن الصفحة مش صفحة تسجيل دخول Instagram
            if r.status_code == 200 and "login" not in r.url:
                results[platform] = full_url
        except:
            continue
    return results
