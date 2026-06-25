# src/agents/auditor.py
from src.state import AgentState
from src.tools.github_tool import fetch_repo_stats

def auditor_node(state: AgentState) -> AgentState:
    """
    Agent A: Fetches hard data from GitHub.
    """
    print(f"--- Auditor Analyzing: {state['repo_url']} ---")
    
    # 1. Call the tool
    data = fetch_repo_stats(state['repo_url'])
    
    # 2. Update state
    # In a complex app, an LLM might analyze this JSON here.
    # For now, we pass the raw data to the synthesizer.
    return {"github_data": data}