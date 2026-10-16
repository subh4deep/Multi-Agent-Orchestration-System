
from backend.app.tools.node_test_runner import run_node_tests


def test_rejects_missing_workspace():
    result = run_node_tests("missing-workspace-folder")

    assert result["passed"] is False
    assert result["exit_code"] is None
    assert result["stderr"] == "Workspace directory does not exist."
