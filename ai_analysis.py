import random

def analyze_ports(domain, open_ports):
    """
    تحليل المنافذ المفتوحة باستخدام ذكاء اصطناعي بسيط (محاكاة)
    """
    if not open_ports:
        return f"لا توجد منافذ مفتوحة على {domain}، الهدف يبدو آمن."

    potential_vulns = {
        21: "FTP Anonymous login possible",
        22: "SSH weak password possible",
        23: "Telnet open - vulnerable",
        80: "HTTP outdated server version",
        443: "HTTPS certificate issues",
        3306: "MySQL default credentials possible",
        3389: "RDP brute force possible"
    }

    analysis = f"تحليل المنافذ المفتوحة على {domain}:\n"
    for port in open_ports:
        vuln = potential_vulns.get(port, "لا توجد ثغرة معروفة لهذا المنفذ")
        analysis += f"- المنفذ {port}: {vuln}\n"

    # إضافة اقتراحات عشوائية للهجوم
    suggestions = [
        "تحقق من كلمات المرور الافتراضية.",
        "فحص الثغرات باستخدام Nmap أو OpenVAS.",
        "تحديث السيرفرات والتطبيقات.",
        "استخدام WAF للحماية من الهجمات."
    ]
    analysis += "\nاقتراحات الهجوم/التدابير:\n"
    for s in random.sample(suggestions, 2):
        analysis += f"- {s}\n"

    return analysis
