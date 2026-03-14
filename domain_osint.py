# domain_osint.py
import dns.resolver
import requests

def whois_lookup(domain):
    """جلب بيانات WHOIS حقيقية عبر RDAP"""
    try:
        r = requests.get(f"https://rdap.org/domain/{domain}", timeout=5)
        if r.status_code == 200:
            return r.json()
        return {"خطأ": "لا توجد بيانات WHOIS"}
    except Exception as e:
        return {"خطأ": str(e)}

def dns_lookup(domain):
    """جلب سجلات DNS حقيقية"""
    records = {}
    for rtype in ["A", "AAAA", "MX", "TXT", "NS"]:
        try:
            ans = dns.resolver.resolve(domain, rtype, lifetime=2)
            records[rtype] = [str(x) for x in ans]
        except:
            records[rtype] = []
    return records

def subdomain_scan(domain):
    """مسح النطاقات الفرعية البسيط"""
    subs = ["www", "mail", "dev", "test", "portal", "admin", "api", "beta"]
    found = {}
    for s in subs:
        host = f"{s}.{domain}"
        try:
            ip = dns.resolver.resolve(host, "A")[0].to_text()
            found[host] = ip
        except:
            continue
    return found
