from src.agents import researcher, user_proxy
from src.config import settings

def start_research(query: str):
    print(f"\n🚀 Starting Research for: '{query}'\n")
    
    # The initiate_chat method triggers the Agentic Loop
    user_proxy.initiate_chat(
        researcher,
        message=f"""I need you to research the following topic in our database: {query}
        Provide a detailed summary and end your final response with 'TERMINATE'."""
    )

if __name__ == "__main__":
    # Example Query: Replace this with something relevant to your PDF!
    user_query = "What are the key findings or main points in the uploaded documents?"
    start_research(user_query)