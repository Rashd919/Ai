def get_key(key):
    value = os.getenv(key)

    if not value:
        try:
            import streamlit as st
            value = st.secrets.get(key)
        except:
            pass

    if not value:
        raise ValueError(f"❌ API KEY MISSING: {key}")

    return value
