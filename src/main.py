"""
Simplified main orchestrator for the research agent.
"""
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir) 
sys.path.insert(0, project_root)

from src.agents import researcher, user_proxy

def start_research(question: str, max_turns: int = 3) -> str:
    """
    Simple research function that handles errors gracefully.
    """
    try:
        print(f"\n[Research] Starting: '{question[:50]}...'")
        
        # Clear previous conversations
        user_proxy.reset()
        researcher.reset()
        
        # Start chat
        chat_result = user_proxy.initiate_chat(
            researcher,
            message=question,
            max_turns=max_turns,
            summary_method="last_msg"
        )
        
        # Try to extract the answer
        if hasattr(chat_result, 'summary'):
            answer = str(chat_result.summary)
        elif hasattr(chat_result, 'chat_history'):
            # Get last message from chat history
            if chat_result.chat_history:
                last_msg = chat_result.chat_history[-1]
                if hasattr(last_msg, 'content'):
                    answer = last_msg.content
                else:
                    answer = str(last_msg)
            else:
                answer = "No conversation history available."
        else:
            # Fallback: try to get from user_proxy's chat_messages
            if researcher in user_proxy.chat_messages:
                messages = user_proxy.chat_messages[researcher]
                if messages:
                    last_msg = messages[-1]
                    if isinstance(last_msg, dict) and 'content' in last_msg:
                        answer = last_msg['content']
                    else:
                        answer = str(last_msg)
                else:
                    answer = "No messages in conversation."
            else:
                answer = "Could not retrieve conversation."
        
        # Clean the answer
        answer = str(answer).replace("TERMINATE", "").strip()
        
        if not answer or len(answer) < 10:
            answer = "I received your query. Please make sure documents are loaded in the knowledge base and try asking a specific question about the available documents."
        
        print(f"[Research] Completed. Answer length: {len(answer)}")
        return answer
        
    except Exception as e:
        error_msg = f"Research error: {str(e)}"
        print(f"[Research] ❌ {error_msg}")
        return f"I apologize, but I encountered an issue: {str(e)[:100]}. Please try again."

# Quick test function
if __name__ == "__main__":
    # Quick test
    test_query = "What can you help me with?"
    print(f"\nTesting with: '{test_query}'")
    
    result = start_research(test_query, max_turns=2)
    print(f"\nResult: {result[:200]}...")
    
    if "error" not in result.lower():
        print("\n✅ System is working!")
    else:
        print("\n❌ System needs troubleshooting")