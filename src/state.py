# src/state.py
from typing import TypedDict, List, Optional
from pydantic import BaseModel, Field

# 1. Define the final structured output
class RiskReport(BaseModel):
    score: int = Field(description="0 to 100 score of project health")
    verdict: str = Field(description="'Invest', 'Hold', or 'Reject'")
    risks: List[str] = Field(description="List of specific technical risks")
    summary: str = Field(description="Executive summary of the findings")

# 2. Define the Graph State (Memory shared between agents)
class AgentState(TypedDict):
    repo_url: str
    github_data: dict      # Data from Auditor
    final_report: Optional[RiskReport] # Final output