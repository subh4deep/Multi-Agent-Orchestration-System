
from backend.app.agents.planner import create_plan
from backend.app.graph.state import WorkflowState
from backend.app.tools.repository_tools import fetch_repository_files
from backend.app.agents.code_generator import generate_patch


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

    patch = generate_patch(issue, state["plan"])

    return {"patch": patch}
