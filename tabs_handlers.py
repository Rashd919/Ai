"""
ملف معالجات التبويبات - تنظيم دوال كل تبويب بشكل منفصل
يساعد في تقليل حجم app.py وتجنب تكرار الـ Keys
"""

import streamlit as st
from utils import (
    get_phone_intelligence, sanitize_text, send_telegram_alert,
    get_geo_data, validate_domain, validate_ip
)
import config
import logging

logger = logging.getLogger(__name__)

# ============= التبويب 0: المحادثة =============
def render_chat_tab():
    """عرض تبويب المحادثة مع Rashd_Ai"""
    st.header("💬 مساعد Rashd_Ai الذكي")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # عرض السجل
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # إدخال المستخدم
    if prompt := st.chat_input("كيف يمكنني مساعدتك اليوم؟", key="chat_input_v1"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                from ai_hacking import AIHackingAssistant
                assistant = AIHackingAssistant()
                response = assistant.chat(prompt)
            except Exception as e:
                response = f"❌ خطأ: {sanitize_text(str(e))}"
            
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

# ============= التبويب 1: تحليل الدومين =============
def render_domain_analysis_tab():
    """عرض تبويب تحليل الدومين"""
    st.header("🌐 تحليل الدومين")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        domain = st.text_input("أدخل اسم الدومين", placeholder="example.com", key="domain_analysis_input_v1")
    with col2:
        analyze_btn = st.button("🔍 تحليل", key="domain_analysis_btn_v1", width='stretch')
    
    if analyze_btn and domain:
        if not validate_domain(domain):
            st.error("❌ صيغة الدومين غير صحيحة")
        else:
            with st.spinner("جاري التحليل..."):
                try:
                    import dns.resolver
                    
                    # محاولة الحصول على سجلات DNS
                    try:
                        a_records = dns.resolver.resolve(domain, 'A')
                        st.success(f"✅ تم العثور على {len(a_records)} سجل A")
                        for record in a_records:
                            st.write(f"IP: {record}")
                    except:
                        st.warning("⚠️ لم يتم العثور على سجلات A")
                
                except Exception as e:
                    st.error(f"❌ خطأ: {sanitize_text(str(e))}")

# ============= التبويب 16: Phone Intelligence =============
def render_phone_intelligence_tab():
    """عرض تبويب Phone Intelligence مع Truecaller"""
    st.header("📱 Phone Intelligence")
    st.write("بحث عن معلومات الهاتف باستخدام Truecaller و Google Dorking")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        phone = st.text_input(
            "أدخل رقم الهاتف",
            placeholder="+966501234567",
            key="phone_intelligence_input_v1"
        )
    with col2:
        search_btn = st.button(
            "🔍 بحث",
            key="phone_intelligence_btn_v1",
            width='stretch'
        )
    
    if search_btn and phone:
        with st.spinner("جاري البحث..."):
            try:
                result = get_phone_intelligence(phone)
                
                # عرض نتائج Truecaller
                if result["truecaller"]["success"]:
                    data = result["truecaller"]["data"]
                    
                    st.success("✅ تم العثور على معلومات!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("📄 المعلومات الأساسية")
                        st.write(f"**الاسم:** {data.get('name', 'Unknown')}")
                        st.write(f"**الهاتف:** {data.get('phone', phone)}")
                        st.write(f"**البريد:** {data.get('email', 'Not Found')}")
                        st.write(f"**الشركة:** {data.get('company', 'Not Found')}")
                    
                    with col2:
                        st.subheader("📸 الصورة")
                        if data.get('image'):
                            try:
                                st.image(data['image'], width=200)
                            except:
                                st.info("⚠️ تعذر تحميل الصورة")
                        else:
                            st.info("لا توجد صورة متاحة")
                    
                    # عرض نتائج Google Dorking
                    if result["google_dork"]["success"] and result["google_dork"]["results"]:
                        st.subheader("🔎 نتائج Google Dorking")
                        for i, res in enumerate(result["google_dork"]["results"], 1):
                            st.write(f"**{i}. {res.get('title', 'No title')}**")
                            st.write(f"   {res.get('href', 'No URL')}")
                else:
                    error_msg = result['truecaller'].get('error', 'خطأ غير معروف')
                    st.error(f"❌ {sanitize_text(error_msg)}")
            
            except Exception as e:
                st.error(f"❌ خطأ: {sanitize_text(str(e))}")
                logger.error(f"Phone Intelligence error: {e}")

# ============= التبويب 17: المصيدة =============
def render_decoy_tab():
    """عرض تبويب المصيدة (Decoy Traps)"""
    st.header("🎯 المصيدة")
    st.write("قم بإنشاء روابط تمويهية لاصطياد الضحايا.")
    
    decoy_type = st.selectbox(
        "اختر نوع المصيدة",
        ["Google Decoy", "Download (APK)", "Download (iOS)"],
        key="decoy_type_select_v1"
    )
    
    if st.button("🎣 إنشاء رابط", key="create_decoy_btn_v1", width='stretch'):
        st.info(f"✅ تم إنشاء رابط {decoy_type}")
        st.code(f"https://rashdai.streamlit.app/?trap={decoy_type.lower().replace(' ', '_')}")
