import random

class AIHackingAssistant:
    def __init__(self):
        self.name = "CyberShield AI Hacking Assistant"

    def analyze_target(self, domain, open_ports=None, tech=None, headers=None):
        """
        تحليل كامل للهدف:
        - المنافذ المفتوحة
        - التقنيات المستخدمة
        - الهيدرز الأمنية
        """
        report = f"🎯 تحليل الهدف: {domain}\n\n"

        # --- المنافذ المفتوحة ---
        if open_ports:
            report += "🔌 المنافذ المفتوحة:\n"
            common_vulns = {
                21: "FTP Anonymous login possible",
                22: "SSH weak password possible",
                23: "Telnet open - vulnerable",
                80: "HTTP outdated server version",
                443: "HTTPS certificate issues",
                3306: "MySQL default credentials possible",
                3389: "RDP brute force possible"
            }
            for port in open_ports:
                vuln = common_vulns.get(port, "لا توجد ثغرة معروفة لهذا المنفذ")
                report += f"- المنفذ {port}: {vuln}\n"
        else:
            report += "🔌 لا توجد معلومات عن المنافذ المفتوحة.\n"

        # --- التقنيات ---
        if tech:
            report += "\n💻 التقنيات المكتشفة:\n"
            for t in tech:
                report += f"- {t}\n"
        else:
            report += "\n💻 لم يتم اكتشاف تقنيات.\n"

        # --- الهيدرز الأمنية ---
        if headers:
            report += "\n🛡️ تحليل الهيدرز الأمنية:\n"
            for k,v in headers.items():
                report += f"- {k}: {v}\n"
        else:
            report += "\n🛡️ لم يتم تحليل الهيدرز.\n"

        # --- اقتراحات هجوم/حماية ---
        suggestions = [
            "تحقق من كلمات المرور الافتراضية.",
            "فحص الثغرات باستخدام Nmap أو OpenVAS.",
            "تحديث السيرفرات والتطبيقات.",
            "استخدام WAF للحماية من الهجمات.",
            "تمكين 2FA على الحسابات الحساسة.",
            "تقييد الوصول عبر IP whitelist."
        ]
        report += "\n💡 اقتراحات إضافية:\n"
        for s in random.sample(suggestions, 3):
            report += f"- {s}\n"

        return report

# تهيئة وحدة الذكاء الاصطناعي الجاهزة للاستخدام
ai_hacking = AIHackingAssistant()
