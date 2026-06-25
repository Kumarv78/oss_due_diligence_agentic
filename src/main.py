# src/main.py
import os
import sys
import warnings

# 1. THE NUCLEAR OPTION: Filter warnings before importing LangChain
os.environ["GRPC_VERBOSITY"] = "ERROR"
warnings.filterwarnings("ignore")

# Now import the rest
from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.agents.auditor import auditor_node
from src.agents.sentiment import sentiment_node
from src.agents.synthesizer import synthesizer_node

# ... (Rest of the file remains exactly the same)

def build_graph():
    workflow = StateGraph(AgentState)
    
    # Add Nodes
    workflow.add_node("auditor", auditor_node)
    workflow.add_node("scout", sentiment_node)      # <--- New Node
    workflow.add_node("synthesizer", synthesizer_node)
    
    # Define Flow: Start -> Auditor AND Scout -> Synthesizer
    workflow.set_entry_point("auditor")
    
    # Create parallel branches (Auditor and Scout run roughly together)
    workflow.add_edge("auditor", "scout") 
    workflow.add_edge("scout", "synthesizer")
    workflow.add_edge("synthesizer", END)
    
    return workflow.compile()

def run_analysis(url: str):
    app = build_graph()
    
    print(f"🚀 Starting Due Diligence on: {url}")
    result = app.invoke({"repo_url": url})
    
    report = result.get("final_report")
    if report:
        print("\n=================================")
        print(f"🏆 VERDICT: {report.verdict.upper()} (Score: {report.score}/100)")
        print("=================================")
        print(f"📝 Summary: {report.summary}")
        print(f"⚠️ Risks: {report.risks}")
    else:
        print("Analysis failed.")

if __name__ == "__main__":
    # Allow running with a URL argument or default to FastAPI
    target_url = sys.argv[1] if len(sys.argv) > 1 else "https://github.com/fastapi/fastapi"
    run_analysis(target_url)