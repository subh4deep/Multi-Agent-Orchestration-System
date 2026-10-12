
from langgraph.graph import StateGraph, START, END

from backend.app.graph.state import WorkflowState
from backend.app.graph.nodes import (
    repository_node,
    planner_node,
    code_generator_node,
)


def build_workflow():
    graph = StateGraph(WorkflowState)

    graph.add_node("repository", repository_node)
    graph.add_node("planner", planner_node)
    graph.add_node("code_generator", code_generator_node)

    graph.add_edge(START, "repository")
    graph.add_edge("repository", "planner")
    graph.add_edge("planner", "code_generator")
    graph.add_edge("code_generator", END)

    return graph.compile()
