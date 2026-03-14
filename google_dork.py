import requests
from bs4 import BeautifulSoup

def search_dork(query):
    """بحث Google Dork متقدم"""
    try:
        url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        results = []
        for g in soup.find_all('a'):
            href = g.get('href')
            if href and href.startswith("http"):
                results.append(href)
        return results[:10]  # أول 10 نتائج
    except Exception as e:
        return {"error": str(e)}
