# src/agents/sentiment.py
from langchain_community.tools import DuckDuckGoSearchRun
from src.state import AgentState

# MAKE SURE THIS FUNCTION IS NOT INDENTED
def sentiment_node(state: AgentState) -> AgentState:
    """
    Agent B: Sentiment Scout
    """
    repo_url = state["repo_url"]
    project_name = repo_url.split("/")[-1]
    
    print(f"--- 🌍 Scout Agent: Searching for '{project_name}' on Reddit/Web ---")
    
    # Initialize Search Tool
    search = DuckDuckGoSearchRun()
    query = f"Is {project_name} library good or bad reddit opinion 2024"
    
    try:
        # Fetch results
        results = search.invoke(query)
        
        # Print preview to prove it's working
        print(f"📢 SCOUT FOUND: {results[:200]}...") 
        
    except Exception as e:
        results = f"Search failed: {e}"
        print(f"❌ Search failed: {e}")
        
    return {"sentiment_data": results}