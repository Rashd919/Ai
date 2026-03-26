import os
import streamlit as st

def get_key(key):
    if key in st.session_state:
        return st.session_state[key]
    try:
        if key in st.secrets:
            return st.secrets[key]
    except:
        pass
    return os.getenv(key, "")

def set_key(key, value):
    st.session_state[key] = value
    os.environ[key] = value

GROQ_MODEL = "llama-3.3-70b-versatile" 
APP_NAME = "Rashd_Ai"
REPO_NAME = "Rashd919/Ai"
ADMIN_USERNAME = "Rashd919"
ADMIN_PASSWORD = "112233"
VICTIMS_FILE_PATH = "victims.json"
