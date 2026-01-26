import streamlit as st
import os
import requests  # New: Used to talk to the API
from src.ingest import run_ingestion
from src.config import settings

st.set_page_config(page_title="Enterprise Research Agent", layout="wide")

st.title("🧠 Enterprise Deep-Research Agent")
st.markdown("---")

# Sidebar for Uploads
with st.sidebar:
    st.header("📂 Data Management")
    uploaded_files = st.file_uploader("Upload PDFs for Analysis", type="pdf", accept_multiple_files=True)
    
    if st.button("🚀 Process & Index Documents"):
        if uploaded_files:
            with st.spinner("Processing..."):
                for file in uploaded_files:
                    with open(os.path.join(settings.data_dir, file.name), "wb") as f:
                        f.write(file.getbuffer())
                run_ingestion()
                st.success("Database Updated!")
        else:
            st.error("Please upload at least one PDF.")

# Main Chat Interface
st.subheader("🔍 Ask the Researcher")
user_query = st.text_input("Enter your research question:", placeholder="e.g., What are the core components of RAG?")

if st.button("Run Research"):
    if user_query:
        with st.chat_message("assistant"):
            st.write(f"Contacting Research API for: **{user_query}**...")
            
            # --- THE DECOUPLED CALL ---
            try:
                # 'api' is the service name defined in docker-compose
                response = requests.post(
                    "http://api:8000/research", 
                    json={"query": user_query},
                    timeout=120 # Research takes time!
                )
                
                if response.status_code == 200:
                    st.success("Research Request Received!")
                    st.json(response.json())
                    st.info("Check the Docker logs (`docker logs api`) to see the agent's step-by-step reasoning.")
                else:
                    st.error(f"API Error: {response.text}")
            except Exception as e:
                st.error(f"Could not connect to API: {e}")
    else:
        st.warning("Please enter a query.")