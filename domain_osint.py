import requests
import socket
import dns.resolver

def whois_lookup(domain):
    """Simple WHOIS lookup via RDAP"""
    try:
        r = requests.get(f"https://rdap.org/domain/{domain}", timeout=5)
        if r.status_code == 200:
            d = r.json()
            return {
                "domain": d.get("ldhName"),
                "status": d.get("status"),
                "events": d.get("events")
            }
    except Exception as e:
        return {"error": str(e)}
    return {}

def dns_lookup(domain):
    records = {}
    for rtype in ["A", "AAAA", "MX", "TXT", "NS"]:
        try:
            ans = dns.resolver.resolve(domain, rtype, lifetime=2)
            records[rtype] = [str(x) for x in ans]
        except:
            records[rtype] = []
    return records

def subdomain_scan(domain):
    """Simple subdomain brute-force"""
    subs = ["www", "mail", "dev", "test", "portal", "admin", "api", "beta", "stage", "m"]
    found = {}
    for s in subs:
        host = f"{s}.{domain}"
        try:
            ip = socket.gethostbyname(host)
            found[host] = ip
        except:
            continue
    return found
