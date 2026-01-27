import autogen
from src.config import settings
from langchain_chroma import Chroma
from langchain_core.embeddings import FakeEmbeddings

# Load the Vector DB
embeddings = FakeEmbeddings(size=1536)
vector_db = Chroma(persist_directory=str(settings.db_dir), embedding_function=embeddings)

def query_knowledge_base(question: str):
    # Only pull 2 chunks to avoid triggering 'Jailbreak' filters with too much text
    docs = vector_db.similarity_search(question, k=2)
    return "\n".join([d.page_content for d in docs])

llm_config = {
    "config_list": [{
        "model": "gpt-4o",
        "api_key": settings.github_token,
        "base_url": "https://models.inference.ai.azure.com"
    }],
    "cache_seed": None, # Disable cache to see real-time changes
}

researcher = autogen.AssistantAgent(
    name="Researcher",
    system_message="You are a helpful assistant. Use the tool to answer questions. End with TERMINATE.",
    llm_config=llm_config,
)

user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    is_termination_msg=lambda x: "TERMINATE" in (x.get("content") or ""),
    code_execution_config=False,
)

autogen.agentchat.register_function(
    query_knowledge_base, caller=researcher, executor=user_proxy,
    name="query_knowledge_base", description="Search the document database"
)