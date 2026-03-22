import os
from fpdf import FPDF
from datetime import datetime
import arabic_reshaper
from bidi.algorithm import get_display

class HackerReport(FPDF):
    def __init__(self):
        super().__init__()
        # مسار الخط الذي يدعم اليونيكود (موجود في المستودع)
        self.font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
        if os.path.exists(self.font_path):
            self.add_font("DejaVu", "", self.font_path, uni=True)
            self.set_font("DejaVu", size=12)
        else:
            self.set_font("Arial", size=12)

    def format_arabic(self, text):
        """تنسيق النص العربي ليظهر بشكل صحيح في PDF"""
        if not text:
            return ""
        reshaped_text = arabic_reshaper.reshape(str(text))
        return get_display(reshaped_text)

    def header(self):
        # خلفية سوداء للهيدر
        self.set_fill_color(0, 0, 0)
        self.rect(0, 0, 210, 30, 'F')
        
        # شعار الهاكر (نص أخضر)
        if os.path.exists(self.font_path):
            self.set_font('DejaVu', '', 16)
        else:
            self.set_font('Arial', 'B', 16)
            
        self.set_text_color(0, 255, 0)
        title = self.format_arabic(">> تقرير CYBERSHIELD PRO - سري للغاية <<")
        self.cell(0, 10, title, 0, 1, 'C')
        
        if os.path.exists(self.font_path):
            self.set_font('DejaVu', '', 10)
        else:
            self.set_font('Arial', '', 10)
            
        self.cell(0, 5, f'TIMESTAMP: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        if os.path.exists(self.font_path):
            self.set_font('DejaVu', '', 8)
        else:
            self.set_font('Arial', 'I', 8)
        self.set_text_color(0, 255, 0)
        footer_text = self.format_arabic(f"الصفحة {self.page_no()} | نهاية الإرسال")
        self.cell(0, 10, footer_text, 0, 0, 'C')

def create_report(data):
    """
    إنشاء تقرير PDF بأسلوب هاكر حقيقي (Matrix Style) مع دعم اللغة العربية.
    """
    pdf = HackerReport()
    pdf.add_page()
    
    # إعدادات الصفحة (خلفية سوداء)
    pdf.set_fill_color(10, 10, 10)
    pdf.rect(0, 30, 210, 267, 'F')
    
    pdf.set_text_color(0, 255, 0) # لون أخضر (Matrix)
    
    # عنوان التقرير
    target = data.get("domain", "UNKNOWN_TARGET")
    if os.path.exists(pdf.font_path):
        pdf.set_font('DejaVu', '', 14)
    else:
        pdf.set_font('Arial', 'B', 14)
        
    title = pdf.format_arabic(f"تحليل الهدف: {target}")
    pdf.cell(0, 10, title, 0, 1, 'L')
    pdf.ln(5)
    
    if os.path.exists(pdf.font_path):
        pdf.set_font('DejaVu', '', 10)
    else:
        pdf.set_font('Arial', '', 10)
    
    # إضافة البيانات
    sections = {
        "بيانات WHOIS": data.get("whois", "لا توجد بيانات"),
        "سجلات DNS": data.get("dns", "لا توجد بيانات"),
        "النطاقات الفرعية": str(data.get("subs", "لا توجد بيانات")),
        "الثغرات المكتشفة": str(data.get("vulns", "لا توجد بيانات")),
        "تحليل الذكاء الاصطناعي": data.get("ai_analysis", "لم يتم إجراء تحليل")
    }
    
    for title, content in sections.items():
        if os.path.exists(pdf.font_path):
            pdf.set_font('DejaVu', '', 12)
        else:
            pdf.set_font('Arial', 'B', 12)
            
        pdf.set_text_color(0, 200, 0)
        section_title = pdf.format_arabic(f"[+] {title}")
        pdf.cell(0, 10, section_title, 0, 1, 'L')
        
        if os.path.exists(pdf.font_path):
            pdf.set_font('DejaVu', '', 9)
        else:
            pdf.set_font('Arial', '', 9)
            
        pdf.set_text_color(0, 255, 0)
        
        # تنظيف المحتوى وتحويله لنص عربي منسق
        text_content = pdf.format_arabic(str(content))
        pdf.multi_cell(0, 5, text_content)
        pdf.ln(5)

    # حفظ الملف
    filename = f"CyberShield_Report_{target}.pdf"
    pdf.output(filename)
    return filename
