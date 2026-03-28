# 📋 دليل النشر والتطوير

هذا الدليل يشرح كيفية نشر وتطوير تطبيق Rashd_Ai.

## 🚀 النشر على Streamlit Cloud

### الخطوة 1: إعداد حساب Streamlit

1. اذهب إلى [streamlit.io](https://streamlit.io)
2. انقر على "Sign Up"
3. استخدم حساب GitHub الخاص بك

### الخطوة 2: ربط المستودع

1. اذهب إلى [Streamlit Community Cloud](https://share.streamlit.io)
2. انقر على "New app"
3. اختر:
   - **Repository:** Rashd919/Ai
   - **Branch:** main
   - **Main file path:** app.py

### الخطوة 3: إضافة المفاتيح السرية

1. انقر على "Advanced settings"
2. أضف المفاتيح السرية:

```toml
GROQ_API_KEY = "your_groq_api_key"
TELEGRAM_BOT_TOKEN = "your_telegram_token"
TELEGRAM_CHAT_ID = "your_chat_id"
TAVILY_API_KEY = "your_tavily_key"
GITHUB_TOKEN = "your_github_token"
```

### الخطوة 4: النشر

انقر على "Deploy" وانتظر انتهاء العملية.

## 🔧 التطوير المحلي

### إعداد بيئة التطوير

```bash
# استنساخ المستودع
git clone https://github.com/Rashd919/Ai.git
cd Ai

# إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate  # على Windows: venv\Scripts\activate

# تثبيت المكتبات
pip install -r requirements.txt

# إنشاء ملف .streamlit/secrets.toml
mkdir -p .streamlit
cat > .streamlit/secrets.toml << 'EOF'
GROQ_API_KEY = "your_key"
TELEGRAM_BOT_TOKEN = "your_token"
TELEGRAM_CHAT_ID = "your_chat_id"
EOF

# تشغيل التطبيق
streamlit run app.py
```

## 📊 هيكل المشروع

```
Ai/
├── app.py                    # التطبيق الرئيسي
├── utils.py                  # الدوال المساعدة
├── config.py                 # الإعدادات
├── ai_hacking.py             # مساعد AI
├── requirements.txt          # المكتبات
├── README.md                 # التوثيق
├── DEPLOYMENT_GUIDE.md       # هذا الملف
├── .streamlit/
│   ├── config.toml          # إعدادات Streamlit
│   └── secrets.toml         # المفاتيح السرية
├── .gitignore               # ملفات Git المتجاهلة
└── .git/                    # مستودع Git
```

## 🔄 دورة التطوير

### 1. إنشاء فرع جديد

```bash
git checkout -b feature/my-feature
```

### 2. إجراء التغييرات

```bash
# تعديل الملفات
# اختبار التطبيق محلياً
streamlit run app.py
```

### 3. فحص الكود

```bash
# فحص الأخطاء النحوية
python -m py_compile *.py

# فحص أسلوب الكود (اختياري)
flake8 *.py

# تنسيق الكود (اختياري)
black *.py
```

### 4. Commit والـ Push

```bash
git add .
git commit -m "وصف التغييرات"
git push origin feature/my-feature
```

### 5. فتح Pull Request

اذهب إلى GitHub وفتح PR لدمج التغييرات.

## 🧪 الاختبار

### اختبار محلي

```bash
# تشغيل التطبيق
streamlit run app.py

# اختبر جميع التبويبات والميزات
# تأكد من عدم وجود أخطاء
```

### اختبار على Streamlit Cloud

1. انشر التطبيق على Streamlit Cloud
2. اختبر جميع الميزات
3. تحقق من السجلات للأخطاء

## 📝 إضافة ميزة جديدة

### مثال: إضافة أداة جديدة

1. **إنشاء ملف جديد** (اختياري):
```python
# my_tool.py
def analyze_target(target):
    """تحليل الهدف"""
    # الكود هنا
    return results
```

2. **إضافة التبويب في app.py**:
```python
# في قسم التبويبات
with tabs[19]:  # رقم التبويب الجديد
    st.header("🔧 أداتي الجديدة")
    # الكود هنا
```

3. **تحديث README.md**:
أضف الأداة الجديدة إلى جدول الأدوات.

4. **Commit والـ Push**:
```bash
git add .
git commit -m "إضافة أداة جديدة"
git push origin feature/new-tool
```

## 🐛 حل المشاكل الشائعة

### المشكلة: "GROQ_API_KEY غير موجود"

**الحل:**
1. تأكد من إضافة المفتاح في `.streamlit/secrets.toml`
2. أعد تشغيل التطبيق

### المشكلة: "خطأ في الاتصال بـ API"

**الحل:**
1. تحقق من الاتصال بالإنترنت
2. تحقق من صحة المفاتيح
3. تحقق من حدود معدل API

### المشكلة: "الصفحة بطيئة جداً"

**الحل:**
1. أضف `@st.cache_data` للدوال الثقيلة
2. قلل عدد الطلبات
3. استخدم معالجة غير متزامنة

## 📚 الموارد المفيدة

- [Streamlit Documentation](https://docs.streamlit.io)
- [Groq API Docs](https://console.groq.com/docs)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [GitHub API](https://docs.github.com/en/rest)

## 🤝 المساهمة

نرحب بالمساهمات! يرجى:

1. Fork المستودع
2. إنشاء فرع جديد
3. إجراء التغييرات
4. فتح Pull Request

## 📞 الدعم

إذا واجهت مشكلة:

1. تحقق من [Issues](https://github.com/Rashd919/Ai/issues)
2. فتح issue جديد إذا لم تجد حلاً
3. اتصل بـ [@Rashd919](https://github.com/Rashd919)

---

آخر تحديث: 28 مارس 2026
