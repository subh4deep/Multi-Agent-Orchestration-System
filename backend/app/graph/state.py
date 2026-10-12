
from typing import TypedDict


class WorkflowState(TypedDict):
    owner: str
    repo_name: str
    issue_number: int
    issue: dict
    repository_files: dict[str, str]
    plan: dict
    patch: str
    test_results: list[str]
    retry_count: int
    approved: bool
