from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display
import os

def create_report(session):
    """إنشاء تقرير PDF من نتائج التحليل مع دعم اللغة العربية"""
    pdf = FPDF()
    pdf.add_page()
    
    # مسار الخط الذي يدعم اليونيكود (موجود في المستودع)
    font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
    
    if os.path.exists(font_path):
        pdf.add_font("DejaVu", "", font_path, uni=True)
        pdf.set_font("DejaVu", size=12)
    else:
        # في حال عدم وجود الخط، نستخدم الخط الافتراضي (قد لا يدعم العربية)
        pdf.set_font("Arial", size=12)
    
    def format_arabic(text):
        """تنسيق النص العربي ليظهر بشكل صحيح في PDF"""
        if not text:
            return ""
        reshaped_text = arabic_reshaper.reshape(str(text))
        return get_display(reshaped_text)

    title = format_arabic("تقرير CyberShield Pro")
    pdf.cell(0, 10, title, ln=True, align="C")
    pdf.ln(10)
    
    for key, value in session.items():
        # تجنب إضافة الكائنات المعقدة أو الصور في هذه المرحلة البسيطة
        if isinstance(value, (str, int, float, list, dict)):
            line_key = format_arabic(f"{key}:")
            pdf.cell(0, 10, line_key, ln=True)
            
            line_val = format_arabic(str(value))
            # استخدام multi_cell للنصوص الطويلة
            pdf.multi_cell(0, 10, line_val)
            pdf.ln(2)
            
    filename = "CyberShield_Report.pdf"
    pdf.output(filename)
    return filename
