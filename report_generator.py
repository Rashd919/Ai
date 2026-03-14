# report_generator.py
# توليد تقرير PDF كامل من نتائج الفحص

from fpdf import FPDF
from datetime import datetime

def create_report(session_state):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "تقرير OSINT وفحص الأمان", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)

    for key, value in session_state.items():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, str(key), ln=True)
        pdf.set_font("Arial", "", 11)
        if isinstance(value, dict):
            for k, v in value.items():
                pdf.cell(0, 7, f"- {k}: {v}", ln=True)
        elif isinstance(value, list):
            for item in value:
                pdf.cell(0, 7, f"- {item}", ln=True)
        else:
            pdf.cell(0, 7, str(value), ln=True)
        pdf.ln(3)

    filename = f"OSINT_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(f"/tmp/{filename}")
    return f"/tmp/{filename}"
