import requests

def username_search(username):
    """
    البحث عن اسم المستخدم على منصات مختلفة
    يرجع قاموس بالمواقع اللي موجود فيها المستخدم
    """
    sites = {
        "GitHub": f"https://github.com/{username}",
        "Reddit": f"https://reddit.com/user/{username}",
        "Pinterest": f"https://pinterest.com/{username}",
        "Medium": f"https://medium.com/@{username}",
        "Instagram": f"https://www.instagram.com/{username}/",
        "Twitter": f"https://twitter.com/{username}"
    }
    found = {}
    for site, url in sites.items():
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                found[site] = url
        except:
            continue
    return found
