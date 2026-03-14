import requests

def email_search(email):
    """كشف التسريبات والحسابات المرتبطة بالبريد"""
    results = {}
    try:
        # مثال: فحص بريد في خدمة HaveIBeenPwned
        r = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}", timeout=5)
        if r.status_code == 200:
            results["Breaches"] = r.json()
        else:
            results["Breaches"] = []
    except:
        results["error"] = "لم يتم العثور على تسريبات أو تعذر الوصول"
    return results
