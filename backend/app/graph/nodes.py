
from backend.app.agents.planner import create_plan
from backend.app.graph.state import WorkflowState


def planner_node(state: WorkflowState) -> dict:
    plan = create_plan(state["issue"])

    return {"plan": plan}
