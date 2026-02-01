import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Go up one level from src/
sys.path.insert(0, project_root)

import streamlit as st
import requests
import time
from src.ingest import run_ingestion
from src.config import settings

# Page configuration
st.set_page_config(
    page_title="Enterprise Research Agent",
    layout="wide",
    page_icon="🧠"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stChatInput {
        margin-top: 2rem;
    }
    .stSpinner > div {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'processing' not in st.session_state:
    st.session_state.processing = False

st.title("🧠 Enterprise Deep-Research Agent")
st.markdown("---")

# Sidebar for Document Management
with st.sidebar:
    st.header("📂 Data Management")
    
    st.subheader("Upload PDFs")
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type="pdf",
        accept_multiple_files=True,
        help="Upload PDF documents for the knowledge base"
    )
    
    if uploaded_files:
        st.info(f"{len(uploaded_files)} file(s) selected for processing")
    
    if st.button("🚀 Process & Index Documents", type="primary"):
        if uploaded_files:
            st.session_state.processing = True
            with st.spinner("Processing and indexing documents..."):
                try:
                    # Save uploaded files to data directory
                    for file in uploaded_files:
                        file_path = os.path.join(settings.data_dir, file.name)
                        with open(file_path, "wb") as f:
                            f.write(file.getbuffer())
                    
                    # Run ingestion process
                    run_ingestion()
                    
                    st.success("✅ Documents processed and database updated!")
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error processing documents: {str(e)}")
                finally:
                    st.session_state.processing = False
        else:
            st.warning("Please upload at least one PDF file first.")
    
    st.markdown("---")
    st.subheader("Knowledge Base Info")
    if os.path.exists(settings.db_dir) and os.listdir(settings.db_dir):
        st.success("✅ Vector database is populated")
    else:
        st.warning("⚠️ No documents indexed yet")

# Main Chat Interface
st.subheader("🔍 Research Assistant")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_query = st.chat_input(
    "Enter your research question...",
    disabled=st.session_state.processing
)

if user_query and not st.session_state.processing:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_query)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🤔 Researching...")
        
        try:
            # Call the API endpoint
            api_url = settings.api_url.rstrip("/") + "/research"
            response = requests.post(
                api_url,
                json={"question": user_query, "max_turns": 3},
                timeout=180  # Research can take time
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get("answer", "No answer received")
                message_placeholder.markdown(answer)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                error_msg = f"API Error {response.status_code}: {response.text}"
                message_placeholder.error(error_msg)
                
        except requests.exceptions.Timeout:
            error_msg = "Research request timed out. Please try again with a more specific question."
            message_placeholder.error(error_msg)
        except requests.exceptions.ConnectionError:
            error_msg = f"Could not connect to the research API. Make sure the API server is running at {settings.api_url}"
            message_placeholder.error(error_msg)
        except Exception as e:
            error_msg = f"An unexpected error occurred: {str(e)}"
            message_placeholder.error(error_msg)

# Clear chat button
if st.session_state.messages and not st.session_state.processing:
    if st.button("Clear Conversation", type="secondary"):
        st.session_state.messages = []
        st.rerun()