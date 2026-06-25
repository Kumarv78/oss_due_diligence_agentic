# src/agents/synthesizer.py
import json
from langchain_ollama import ChatOllama
from src.state import AgentState, RiskReport

# Initialize Local Model (Llama 3.2)
# temperature=0 makes it deterministic (good for JSON)
llm = ChatOllama(
    model="llama3.2", 
    temperature=0,
    format="json" 
)

def synthesizer_node(state: AgentState) -> AgentState:
    print("--- 🧠 Investment Partner: Generating Verdict (Local LLM) ---")
    
    # 1. Get BOTH data sources
    github_stats = state.get("github_data")
    sentiment = state.get("sentiment_data", "No sentiment data found.")
    
    # 2. Updated Prompt to include Sentiment
    system_msg = """
    You are a Senior Technical Due Diligence Officer.
    
    INSTRUCTIONS:
    1. Analyze the 'github_data' (Hard Metrics).
    2. Analyze the 'sentiment_data' (Soft Metrics).
    
    SCORING RULES:
    - If 'last_update' > 1 year, REJECT immediately.
    - If 'stars' > 10000 but sentiment says "buggy" or "abandoned", SCORE LOW (40-50) and HOLD.
    - If sentiment is positive ("love it", "standard", "great"), BOOST the score.

    OUTPUT FORMAT (JSON ONLY):
    {
        "score": (int 0-100),
        "verdict": ("Invest", "Hold", or "Reject"),
        "risks": ["list", "of", "risks", "from", "sentiment", "or", "stats"],
        "summary": "Explain your decision referencing BOTH GitHub stats and Reddit sentiment."
    }
    """
    
    response = llm.invoke([
        ("system", system_msg),
        ("human", f"GitHub Stats: {github_stats}\n\nSentiment Search Results: {sentiment}")
    ])
    
    # (Parsing logic stays the same...)
    import json
    try:
        content_dict = json.loads(response.content)
        report = RiskReport(**content_dict)
        return {"final_report": report}
    except Exception as e:
        print(f"❌ JSON Parsing Failed: {e}")
        return {"final_report": RiskReport(score=0, verdict="Error", risks=[], summary="Error")}