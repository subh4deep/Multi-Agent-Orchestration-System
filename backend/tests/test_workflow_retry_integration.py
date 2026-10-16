
from unittest.mock import patch

from backend.app.graph.workflow import build_workflow


def test_workflow_retries_after_failed_attempt():
    initial_state = {
        "owner": "test-owner",
        "repo_name": "test-repo",
        "issue_number": 1,
        "issue": {
            "number": 1,
            "title": "Fix greeting",
            "body": "Return the correct greeting.",
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

    fake_files = {"app.py": 'def greet():\n    return "hello"\n'}

    fake_plan = {
        "summary": "Fix greeting",
        "steps": ["Update greet"],
        "testing": ["Run tests"],
    }

    fake_patch = "--- a/app.py\n+++ b/app.py\n@@ -1 +1 @@\n-old\n+new\n"

    failed_result = {
        "patch_validation": {"valid": True, "files": ["app.py"], "error": None},
        "patch_application": {"success": True, "error": None},
        "test_results": [
            {
                "passed": False,
                "exit_code": 1,
                "stdout": "",
                "stderr": "AssertionError",
            }
        ],
        "tests_passed": False,
    }

    successful_result = {
        "patch_validation": {"valid": True, "files": ["app.py"], "error": None},
        "patch_application": {"success": True, "error": None},
        "test_results": [
            {
                "passed": True,
                "exit_code": 0,
                "stdout": "1 passed",
                "stderr": "",
            }
        ],
        "tests_passed": True,
    }

    with (
        patch(
            "backend.app.graph.nodes.fetch_repository_files",
            return_value=fake_files,
        ),
        patch(
            "backend.app.graph.nodes.create_plan",
            return_value=fake_plan,
        ),
        patch(
            "backend.app.graph.nodes.generate_patch",
            side_effect=[fake_patch, fake_patch],
        ) as mock_generator,
        patch(
            "backend.app.graph.nodes.execute_patch_pipeline",
            side_effect=[failed_result, successful_result],
        ),
    ):
        workflow = build_workflow()
        result = workflow.invoke(initial_state)


    assert mock_generator.call_count == 2
    assert result["retry_count"] == 1
    assert result["tests_passed"] is True

    second_call = mock_generator.call_args_list[1]
    second_issue = second_call.args[0]

    assert "previous_attempt_feedback" in second_issue
    assert second_issue["previous_attempt_feedback"]["test_results"][0]["stderr"] == "AssertionError"

