import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Go up one level from src/
sys.path.insert(0, project_root)

import autogen
from autogen import AssistantAgent, UserProxyAgent
from typing import Optional
from src.config import settings
from langchain_chroma import Chroma
from langchain_core.embeddings import FakeEmbeddings

# Load the Vector DB
embeddings = FakeEmbeddings(size=1536)
vector_db = Chroma(persist_directory=str(settings.db_dir), embedding_function=embeddings)

def query_knowledge_base(question: str) -> str:
    """
    Query the vector database for relevant document chunks.
    
    Args:
        question: The research question to search for
        
    Returns:
        Concatenated relevant document chunks as a string
    """
    try:
        # Only pull 2 chunks to avoid triggering 'Jailbreak' filters with too much text
        docs = vector_db.similarity_search(question, k=2)
        if not docs:
            return "No relevant documents found in the knowledge base."
        return "\n\n".join([f"Document {i+1}:\n{d.page_content}" for i, d in enumerate(docs)])
    except Exception as e:
        return f"Error querying knowledge base: {str(e)}"

# LLM configuration for AutoGen
llm_config = {
    "config_list": [{
        "model": "gpt-4o",
        "api_key": settings.github_token,
        "base_url": "https://models.inference.ai.azure.com"
    }],
    "cache_seed": None,  # Disable cache to see real-time changes
    "temperature": 0.3,  # Added for more focused responses
    "timeout": 120,      # Added timeout for API calls
}

# Create the research assistant agent
researcher = AssistantAgent(
    name="Researcher",
    system_message="""You are a helpful research assistant. Use the query_knowledge_base tool 
    to search through the document database for relevant information. Analyze the retrieved 
    information and provide comprehensive, accurate answers. When you have provided a complete 
    answer based on the available documents, end your response with TERMINATE.""",
    llm_config=llm_config,
)

# Create the user proxy agent (handles tool execution)
user_proxy = UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    is_termination_msg=lambda x: x and "TERMINATE" in (x.get("content") or "") if isinstance(x, dict) else False,
    code_execution_config=False,
)

# Register the knowledge base query function as a tool
autogen.register_function(
    query_knowledge_base,
    caller=researcher,
    executor=user_proxy,
    name="query_knowledge_base",
    description="Search the document database for information related to a question. Returns relevant document chunks."
)