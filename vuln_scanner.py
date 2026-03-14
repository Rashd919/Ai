def scan_vulnerabilities(target):
    """محاكي اكتشاف الثغرات"""
    return [
        {"vuln": "CVE-2023-12345", "severity": "High", "target": target},
        {"vuln": "CVE-2022-54321", "severity": "Medium", "target": target}
    ]
