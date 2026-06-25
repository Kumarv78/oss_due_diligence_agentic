# 🕵️ Open Source Technical Due Diligence Agent

An autonomous, multi-agent AI system designed to perform technical due diligence on open-source repositories. This tool acts as an "AI Analyst" for CTOs and VC firms, evaluating code health, maintainer activity, and community sentiment to generate a final adoption/investment verdict.

## 🏗️ System Architecture

The pipeline is orchestrated using **LangGraph** and utilizes a local LLM for private, cost-effective reasoning.

1. **Auditor Agent:** Queries the GitHub API to extract hard metrics (stars, open issues, fork ratio, time since last commit).
2. **Scout Agent:** Leverages the Tavily Search API to scan Reddit, Dev.to, and HackerNews for real-time community sentiment and potential red flags.
3. **Investment Partner (Synthesizer):** A local LLM (Llama 3.2 via Ollama) that ingests both hard and soft metrics, reasons through the data, and outputs a strictly typed JSON verdict (Invest, Hold, or Reject) with a confidence score.

## 🛠️ Tech Stack
* **Orchestration:** LangGraph, LangChain
* **LLM:** Ollama (Llama 3.2) - *Zero API cost & complete data privacy*
* **Tools:** PyGithub, Tavily Search API
* **Data Validation:** Pydantic
* **Dependency Management:** Poetry

## 📂 Project Structure
```text
oss-due-diligence/
├── src/
│   ├── main.py                 # Graph orchestration & entry point
│   ├── state.py                # Pydantic models & Graph State definition
│   ├── agents/
│   │   ├── auditor.py          # GitHub metrics extraction
│   │   ├── sentiment.py        # Web search & sentiment analysis
│   │   └── synthesizer.py      # LLM reasoning & structured output
│   └── tools/
│       └── github_tool.py      # GitHub API wrapper
├── tests/                      # Pytest suite
├── pyproject.toml              # Poetry dependencies
└── .env                        # Environment secrets