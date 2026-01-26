import autogen
from src.config import settings
from langchain_community.vectorstores import Chroma
from langchain_core.embeddings import FakeEmbeddings

# 1. Setup the Vector Database Connection
# We use the same settings as ingest.py so they talk to the same "Brain"
embeddings = FakeEmbeddings(size=1536)
vector_db = Chroma(
    persist_directory=str(settings.db_dir), 
    embedding_function=embeddings
)

# 2. Define the Search Tool
def query_knowledge_base(question: str):
    """Searches the enterprise PDF database for specific information."""
    docs = vector_db.similarity_search(question, k=3)
    return "\n---\n".join([d.page_content for d in docs])

# 3. Configure the LLM
llm_config = {
    "config_list": [{"model": "gpt-4o", "api_key": settings.github_token, "base_url": "https://models.inference.ai.azure.com"}],
    "cache_seed": 42,
}

# 4. Define the Agents
researcher = autogen.AssistantAgent(
    name="Researcher",
    system_message="""You are an Expert Researcher. 
    Use the 'query_knowledge_base' tool to find facts in our documents. 
    Always cite your findings. If the answer isn't in the database, say you don't know.""",
    llm_config=llm_config,
)

user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "research_output", "use_docker": settings.use_docker},
)

# 5. Register the tool so the agent can actually use it
autogen.agentchat.register_function(
    query_knowledge_base,
    caller=researcher,
    executor=user_proxy,
    name="query_knowledge_base",
    description="A tool to search the enterprise document database",
)