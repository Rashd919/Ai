from fpdf import FPDF

def create_report(session):
    """إنشاء تقرير PDF من نتائج التحليل"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "تقرير CyberShield Pro", ln=True, align="C")
    pdf.ln(10)
    for key, value in session.items():
        pdf.cell(0, 10, f"{key}: {value}", ln=True)
    filename = "CyberShield_Report.pdf"
    pdf.output(filename)
    return filename
