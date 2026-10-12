from backend.app.tools.github_client import fetch_issue


def test_fetch_github_issue():
    issue = fetch_issue(
        owner="subh4deep",
        repo_name="ResumeX",
        issue_number=1,
    )

    assert issue["number"] == 1
    assert issue["title"]
    assert issue["url"].startswith("https://github.com/")