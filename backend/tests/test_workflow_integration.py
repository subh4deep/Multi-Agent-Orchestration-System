
from unittest.mock import patch

from backend.app.graph.workflow import build_workflow


def test_workflow_completes_successfully():
    repository_files = {
        "app.py": 'def greet():\n    return "hello"\n',
        "test_app.py": (
            "from app import greet\n\n"
            "def test_greet():\n"
            '    assert greet() == "hello"\n'
        ),
    }
    fake_patch = (
        "--- a/app.py\n"
        "+++ b/app.py\n"
        "@@ -1,2 +1,2 @@\n"
        "-def greet():\n"
        '-    return "hello"\n'
        "+def greet():\n"
        '+    return "hello"\n'
    )

    initial_state = {
        "owner": "test-owner",
        "repo_name": "test-repo",
        "issue_number": 1,
        "issue": {
            "number": 1,
            "title": "Update greeting",
            "body": "Change the greeting.",
        },
        "repository_files": {},
        "plan": {},
        "patch": "",
        "patch_validation": {},
        "patch_application": {},
        "test_results": [],
        "tests_passed": False,
        "retry_count": 0,
        "approved": False,
    }

    with (
        patch(
            "backend.app.graph.nodes.fetch_repository_files",
            return_value=repository_files,
        ),
        patch(
            "backend.app.graph.nodes.create_plan",
            return_value={
                "summary": "Update greeting",
                "steps": ["Change the greeting"],
                "testing": ["Run tests"],
            },
        ),
        patch(
            "backend.app.graph.nodes.generate_patch",
            return_value=fake_patch,
        ),
    ):
        workflow = build_workflow()
        result = workflow.invoke(initial_state)

    print("Patch validation:", result["patch_validation"])
    print("Patch application:", result["patch_application"])
    print("Test results:", result["test_results"])

    assert result["patch_validation"]["valid"] is True
    assert result["patch_application"]["success"] is True
    assert result["tests_passed"] is True
    assert result["project_info"]["language"] == "python"