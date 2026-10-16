
from backend.app.tools.test_runner_selector import select_test_command
from backend.app.tools.project_detector import detect_project
from backend.app.tools.patch_validator import validate_patch
from backend.app.tools.workspace_manager import (
    create_workspace,
    cleanup_workspace,
)
from backend.app.tools.patch_applier import apply_patch
from backend.app.tools.test_runner import run_tests


def execute_patch_pipeline(
    repository_files: dict[str, str],
    patch: str,
) -> dict:
    validation = validate_patch(patch, repository_files)

    if not validation["valid"]:
        return {
            "patch_validation": validation,
            "patch_application": {
                "success": False,
                "error": "Patch failed validation.",
            },
            "test_results": [],
            "tests_passed": False,
        }

    workspace = create_workspace(repository_files)

    try:
        application = apply_patch(workspace, patch)

        if not application["success"]:
            return {
                "patch_validation": validation,
                "patch_application": application,
                "test_results": [],
                "tests_passed": False,
            }
        project_info = detect_project(workspace)
        test_command = select_test_command(project_info)

        if test_command is None:
            return {
                "patch_validation": validation,
                "patch_application": application,
                "project_info": project_info,
                "test_results": [{
                    "passed": False,
                    "exit_code": None,
                    "stdout": "",
                    "stderr": "No supported test runner detected.",
                }],
                "tests_passed": False,
            }

        if test_command != "pytest":
            return {
                "patch_validation": validation,
                "patch_application": application,
                "project_info": project_info,
                "test_results": [{
                    "passed": False,
                    "exit_code": None,
                    "stdout": "",
                    "stderr": f"Test runner '{test_command}' is detected but not yet supported.",
                }],
                "tests_passed": False,
            }

        test_result = run_tests(workspace, test_command=test_command)

        return {
            "patch_validation": validation,
            "patch_application": application,
            "project_info": project_info,
            "test_results": [test_result],
            "tests_passed": test_result["passed"],
            "project_info": project_info,
        }

    finally:
        cleanup_workspace(workspace)
