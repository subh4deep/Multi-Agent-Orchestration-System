
from langgraph.graph import StateGraph, START, END

from backend.app.graph.state import WorkflowState
from backend.app.graph.nodes import (
    repository_node,
    planner_node,
    code_generator_node,
    execution_node,
    retry_node,
)

MAX_RETRIES = 2


def route_after_execution(state: WorkflowState) -> str:
    if state.get("tests_passed", False):
        return "end"

    if state.get("retry_count", 0) >= MAX_RETRIES:
        return "end"

    return "retry"


def build_workflow():
    graph = StateGraph(WorkflowState)

    graph.add_node("repository", repository_node)
    graph.add_node("planner", planner_node)
    graph.add_node("code_generator", code_generator_node)
    graph.add_node("execution", execution_node)
    graph.add_node("retry", retry_node)

    graph.add_edge(START, "repository")
    graph.add_edge("repository", "planner")
    graph.add_edge("planner", "code_generator")
    graph.add_edge("code_generator", "execution")

    graph.add_conditional_edges(
        "execution",
        route_after_execution,
        {
            "retry": "retry",
            "end": END,
        },
    )

    graph.add_edge("retry", "code_generator")

    return graph.compile()
