import requests

def username_search(username):
    """البحث عن اسم مستخدم في منصات مختلفة والتحقق من وجوده فعلياً"""
    base_urls = {
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}",
        "Pinterest": f"https://pinterest.com/{username}",
        "GitHub": f"https://github.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Facebook": f"https://www.facebook.com/{username}",
        "LinkedIn": f"https://www.linkedin.com/in/{username}",
        "YouTube": f"https://www.youtube.com/{username}",
        "Snapchat": f"https://www.snapchat.com/add/{username}",
        "Medium": f"https://medium.com/@{username}",
        "Twitch": f"https://www.twitch.tv/{username}",
        "SoundCloud": f"https://soundcloud.com/{username}",
        "VK": f"https://vk.com/{username}",
        "GitLab": f"https://gitlab.com/{username}"
    }

    results = {}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    for platform, url in base_urls.items():
        try:
            r = requests.get(url, headers=headers, timeout=5)
            if r.status_code == 200:
                results[platform] = url  # الحساب موجود
        except:
            continue

    if not results:
        return "لا يوجد نتائج للحساب."
    return results
