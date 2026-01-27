from src.agents import researcher, user_proxy

def start_research(query: str):
    # Start the conversation
    chat_result = user_proxy.initiate_chat(
        researcher,
        message=f"Find information about: {query}",
        summary_method="last_msg"
    )
    return chat_result.summary