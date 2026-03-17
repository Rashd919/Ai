import requests
import os
from config import get_key
from dotenv import load_dotenv

load_dotenv()

def email_search(email):
    """كشف التسريبات والحسابات المرتبطة بالبريد باستخدام Tavily وخدمات أخرى"""
    results = {}

    # ✅ خذ المفتاح من env أو secrets
    api_key = get_key("TAVILY_API_KEY")

    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("TAVILY_API_KEY")
        except:
            pass

    if not api_key:
        return {"error": "❌ TAVILY_API_KEY غير موجود لا في env ولا في secrets"}

    try:
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": api_key,
            "query": f"email leak breach data for {email}",
            "search_depth": "advanced",
            "include_answer": True
        }

        response = requests.post(url, json=payload, timeout=10)

        if response.status_code == 200:
            data = response.json()
            results["Tavily_Analysis"] = data.get("answer", "لم يتم العثور على تحليل مباشر")
            results["Search_Results"] = []

            for r in data.get("results", []):
                results["Search_Results"].append({
                    "title": r.get("title"),
                    "url": r.get("url"),
                    "snippet": r.get("content")
                })
        else:
            results["error"] = f"خطأ في Tavily: {response.status_code}"

    except Exception as e:
        results["error"] = f"خطأ: {str(e)}"

    return results
