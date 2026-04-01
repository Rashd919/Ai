# ============= التبويب 16: Phone Intelligence =============
# هذا الملف يحتوي على كود تبويب Phone Intelligence

def render_phone_intelligence_tab(tabs):
    """عرض تبويب Phone Intelligence بالبحث الهجين المتقدم"""
    import streamlit as st
    from utils import search_phone_hybrid, search_data_leaks_phone
    
    with tabs[16]:
        st.header("📱 Phone Intelligence - البحث الهجين المتقدم")
        st.write("🔍 بحث شامل عن معلومات الهاتف: الهوية + الحسابات الاجتماعية + تسريبات البيانات")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            phone = st.text_input("أدخل رقم الهاتف", placeholder="+962775866283", key="phone_intelligence_hybrid_input_v1")
        with col2:
            search_btn = st.button("🔍 بحث شامل", key="phone_intelligence_hybrid_btn_v1", width='stretch')
        
        if search_btn and phone:
            with st.spinner("⏳ جاري البحث الهجين المتقدم (قد يستغرق 30 ثانية)..."):
                try:
                    # البحث الهجين
                    hybrid_result = search_phone_hybrid(phone)
                    
                    if hybrid_result.get("success"):
                        data = hybrid_result.get("data", {})
                        
                        # عرض الملخص
                        st.success(f"✅ {data.get('summary', 'تم إجراء البحث')}")
                        
                        # التبويبات الفرعية
                        tab_identity, tab_social, tab_leaks = st.tabs(["👤 الهوية", "📱 الحسابات الاجتماعية", "⚠️ التسريبات"])
                        
                        # تبويب الهوية
                        with tab_identity:
                            st.subheader("معلومات الهوية المكتشفة")
                            identity_data = data.get("identity", {})
                            if identity_data:
                                for query, info in identity_data.items():
                                    st.write(f"**{query}:**")
                                    st.write(f"العنوان: {info.get('title', 'N/A')}")
                                    st.write(f"الوصف: {info.get('body', 'N/A')}")
                                    st.divider()
                            else:
                                st.info("لم يتم العثور على معلومات هوية")
                        
                        # تبويب الحسابات الاجتماعية
                        with tab_social:
                            st.subheader("الحسابات الاجتماعية المرتبطة")
                            social_accounts = data.get("social_accounts", [])
                            if social_accounts:
                                for account in social_accounts:
                                    col1, col2 = st.columns([1, 3])
                                    with col1:
                                        st.write(f"📱 {account.get('platform', 'Unknown').upper()}")
                                    with col2:
                                        if account.get('url'):
                                            st.write(f"[الرابط]({account.get('url')})")
                                        else:
                                            st.write("لم يتم العثور على رابط")
                            else:
                                st.info("لم يتم العثور على حسابات اجتماعية")
                        
                        # تبويب التسريبات
                        with tab_leaks:
                            st.subheader("تسريبات البيانات المكتشفة")
                            leaks = data.get("leaks", {})
                            
                            # DeHashed
                            dehashed_leaks = leaks.get("dehashed", [])
                            if dehashed_leaks:
                                st.warning(f"⚠️ تم العثور على {len(dehashed_leaks)} تسريب في DeHashed")
                                for i, leak in enumerate(dehashed_leaks, 1):
                                    with st.expander(f"التسريب #{i} - {leak.get('database', 'Unknown')}"):
                                        st.write(f"**البريد:** {leak.get('email', 'N/A')}")
                                        st.write(f"**اسم المستخدم:** {leak.get('username', 'N/A')}")
                                        st.write(f"**الاسم:** {leak.get('name', 'N/A')}")
                                        st.write(f"**قاعدة البيانات:** {leak.get('database', 'Unknown')}")
                            
                            # Tavily
                            tavily_leaks = leaks.get("tavily", [])
                            if tavily_leaks:
                                st.info(f"ℹ️ تم العثور على {len(tavily_leaks)} نتيجة في Tavily")
                                for i, leak in enumerate(tavily_leaks, 1):
                                    with st.expander(f"النتيجة #{i}"):
                                        st.write(f"**العنوان:** {leak.get('title', 'N/A')}")
                                        st.write(f"**الوصف:** {leak.get('snippet', 'N/A')}")
                                        if leak.get('url'):
                                            st.write(f"[الرابط]({leak.get('url')})")
                            
                            if not dehashed_leaks and not tavily_leaks:
                                st.success("✅ لم يتم العثور على تسريبات معروفة")
                    else:
                        st.error(f"❌ {hybrid_result.get('error', 'خطأ في البحث')}")
                
                except Exception as e:
                    st.error(f"❌ خطأ في البحث: {str(e)}")
