# src/tools/github_tool.py
import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

def fetch_repo_stats(repo_url: str):
    """
    Extracts owner/repo from URL and fetches stats using PyGithub.
    """
    try:
        g = Github(os.getenv("GITHUB_TOKEN"))
        
        # Clean URL to get "owner/repo"
        repo_path = repo_url.replace("https://github.com/", "").strip("/")
        repo = g.get_repo(repo_path)
        
        stats = {
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "open_issues": repo.open_issues_count,
            "last_update": str(repo.updated_at),
            "created_at": str(repo.created_at),
            "description": repo.description
        }
        return stats
    except Exception as e:
        return {"error": str(e)}