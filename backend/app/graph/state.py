
from typing import TypedDict


class WorkflowState(TypedDict):
    owner: str
    repo_name: str
    issue_number: int
    issue: dict
    repository_files: dict[str, str]
    plan: dict
    patch: str
    patch_validation: dict
    patch_application: dict
    test_results: list[dict]
    tests_passed: bool
    retry_count: int
    approved: bool
    project_info: dict | None
