
from backend.app.agents.planner import create_plan
from backend.app.graph.state import WorkflowState
from backend.app.tools.repository_tools import fetch_repository_files
from backend.app.agents.code_generator import generate_patch
from backend.app.tools.patch_validator import validate_patch
from backend.app.graph.execution import execute_patch_pipeline


def repository_node(state: WorkflowState) -> dict:
    files = fetch_repository_files(
        owner=state["owner"],
        repo_name=state["repo_name"],
    )

    return {"repository_files": files}


def planner_node(state: WorkflowState) -> dict:
    issue = dict(state["issue"])
    issue["repository_files"] = state["repository_files"]

    plan = create_plan(issue)

    return {"plan": plan}


def code_generator_node(state: WorkflowState) -> dict:
    issue = dict(state["issue"])
    issue["repository_files"] = state["repository_files"]

    if state.get("retry_count", 0) > 0:
        issue["previous_attempt_feedback"] = {
            "patch_validation": state.get("patch_validation", {}),
            "patch_application": state.get("patch_application", {}),
            "test_results": state.get("test_results", []),
        }

    patch = generate_patch(issue, state["plan"])
    return {"patch": patch}


def patch_validation_node(state: WorkflowState) -> dict:
    validation = validate_patch(
        patch=state["patch"],
        repository_files=state["repository_files"],
    )

    return {"patch_validation": validation}




def execution_node(state: WorkflowState) -> dict:
    result = execute_patch_pipeline(
        repository_files=state["repository_files"],
        patch=state["patch"],
    )
    return {
        "patch_validation": result["patch_validation"],
        "patch_application": result["patch_application"],
        "test_results": result["test_results"],
        "tests_passed": result["tests_passed"],
        "project_info": result.get("project_info"),
    }




def retry_node(state: WorkflowState) -> dict:
    return {"retry_count": state.get("retry_count", 0) + 1}

