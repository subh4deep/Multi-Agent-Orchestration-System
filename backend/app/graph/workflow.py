
from langgraph.graph import StateGraph, START, END

from backend.app.graph.state import WorkflowState
from backend.app.graph.nodes import planner_node


def build_workflow():
    graph = StateGraph(WorkflowState)

    graph.add_node("planner", planner_node)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", END)

    return graph.compile()
