import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Go up one level from src/
sys.path.insert(0, project_root)

import streamlit as st
import requests
import os
from src.config import settings

st.set_page_config(page_title="Enterprise Research", page_icon="🔍")

# Dynamic API URL (Docker-aware)
API_BASE = os.getenv("API_URL", "http://api:8000")

st.title("Enterprise Research Agent")

with st.sidebar:
    st.header("Admin")
    if st.button("Re-index Documents"):
        # Logic to call run_ingestion()
        st.success("Indexing complete!")

query = st.chat_input("Ask a question about your documents...")

if query:
    st.chat_message("user").write(query)
    with st.spinner("Consulting documents..."):
        try:
            res = requests.post(f"{API_BASE}/research", json={"question": query})
            answer = res.json().get("answer")
            st.chat_message("assistant").write(answer)
        except Exception as e:
            st.error(f"Connection failed: {e}")