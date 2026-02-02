import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Go up one level from src/
sys.path.insert(0, project_root)

import autogen
from autogen import AssistantAgent, UserProxyAgent, register_function
from src.config import settings
from langchain_chroma import Chroma
from langchain_core.embeddings import FakeEmbeddings

# Configuration
llm_config = {
    "config_list": [{
        "model": "gpt-4o",
        "api_key": settings.github_token,
        "base_url": "https://models.inference.ai.azure.com"
    }],
    "temperature": 0.1,
}

# Agents
researcher = AssistantAgent(
    name="Researcher",
    system_message="""You are an expert Research Assistant. 
    1. Search the knowledge base for facts.
    2. If the info isn't there, say so.
    3. Provide a final summary and end with TERMINATE.""",
    llm_config=llm_config,
)

user_proxy = UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda x: "TERMINATE" in (x.get("content") or ""),
    code_execution_config=False,
)

# Tool Definition
def query_knowledge_base(question: str) -> str:
    # Use real embeddings here in production
    db = Chroma(persist_directory=str(settings.db_dir), embeddings = FakeEmbeddings(size=1536))
    docs = db.similarity_search(question, k=3)
    return "\n\n".join([d.page_content for d in docs]) if docs else "No info found."

# Registration
register_function(
    query_knowledge_base,
    caller=researcher,
    executor=user_proxy,
    name="query_knowledge_base",
    description="Queries the enterprise internal PDF database."
)