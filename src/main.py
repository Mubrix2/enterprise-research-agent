"""
Simplified main orchestrator for the research agent.
"""
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir) 
sys.path.insert(0, project_root)

from src.agents import researcher, user_proxy

def start_research(question: str) -> str:
    user_proxy.reset()
    researcher.reset()
    
    result = user_proxy.initiate_chat(
        researcher,
        message=question,
        clear_history=True,
        summary_method="last_msg"
    )
    
    # Extract content safely
    answer = result.summary if result.summary else "I couldn't find a specific answer."
    return answer.replace("TERMINATE", "").strip()