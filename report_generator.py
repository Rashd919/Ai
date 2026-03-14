from fpdf import FPDF
from datetime import datetime
import tempfile

class PDFReportGenerator:
    def __init__(self):
        self.font_path = "DejaVuSans.ttf"  # ضع الخط في نفس مجلد المشروع أو مسار صحيح

    def create_report(self, session_data):
        """
        إنشاء تقرير PDF كامل من بيانات session_state
        """
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu', '', self.font_path, uni=True)
        pdf.set_font("DejaVu", '', 16)
        pdf.set_text_color(200,0,0)
        pdf.cell(0, 10, "CyberShield Pro OSINT Report", ln=True, align="C")

        pdf.set_font("DejaVu", '', 12)
        pdf.set_text_color(0,0,0)
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        pdf.cell(0, 10, f"Report Date: {date}", ln=True)

        pdf.ln(5)
        pdf.set_font("DejaVu", '', 14)
        pdf.cell(0, 10, "Session Data Overview:", ln=True)

        pdf.set_font("DejaVu", '', 11)
        for key, value in session_data.items():
            pdf.multi_cell(0, 8, f"{key}: {value}")
            pdf.ln(2)

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf.output(temp_file.name)
        return temp_file.name

# لتسهيل الاستخدام:
report_generator = PDFReportGenerator()
