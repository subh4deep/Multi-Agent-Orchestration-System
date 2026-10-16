from github import Github, Auth
from backend.app.config import settings


def get_github_client():
    if not settings.github_token:
        raise ValueError("GITHUB_TOKEN is missing from .env")

    auth = Auth.Token(settings.github_token)
    return Github(auth=auth)

def fetch_issue(owner: str, repo_name: str, issue_number: int):
    client = get_github_client()
    repo = client.get_repo(f"{owner}/{repo_name}")
    issue = repo.get_issue(number=issue_number)

    return {
        "number": issue.number,
        "title": issue.title,
        "body": issue.body or "",
        "state": issue.state,
        "url": issue.html_url,
    }
