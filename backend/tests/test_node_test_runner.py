
import subprocess
from unittest.mock import patch, MagicMock

from backend.app.tools.node_test_runner import run_node_tests


def test_rejects_missing_workspace():
    result = run_node_tests("missing-workspace-folder")

    assert result["passed"] is False
    assert result["exit_code"] is None
    assert result["stderr"] == "Workspace directory does not exist."


def test_rejects_missing_package_json(tmp_path):
    result = run_node_tests(str(tmp_path))

    assert result["passed"] is False
    assert result["exit_code"] is None
    assert result["stderr"] == "package.json not found."


def test_runs_tests_in_docker(tmp_path):
    (tmp_path / "package.json").write_text(
        '{"scripts": {"test": "jest"}}',
        encoding="utf-8",
    )

    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "Tests passed"
    mock_result.stderr = ""

    with patch(
        "backend.app.tools.node_test_runner.subprocess.run",
        return_value=mock_result,
    ) as mock_run:
        result = run_node_tests(str(tmp_path))

    assert result["passed"] is True
    assert result["exit_code"] == 0
    assert result["stdout"] == "Tests passed"

    command = mock_run.call_args.args[0]
    assert command[0] == "docker"
    assert "--network" in command
    assert "none" in command
    assert "npm" in command
    assert mock_run.call_args.kwargs["shell"] is False


def test_handles_timeout(tmp_path):
    (tmp_path / "package.json").write_text(
        '{"scripts": {"test": "jest"}}',
        encoding="utf-8",
    )

    with patch(
        "backend.app.tools.node_test_runner.subprocess.run",
        side_effect=subprocess.TimeoutExpired("docker", 60),
    ):
        result = run_node_tests(str(tmp_path))

    assert result["passed"] is False
    assert result["exit_code"] is None
    assert "timed out" in result["stderr"]


def test_handles_docker_unavailable(tmp_path):
    (tmp_path / "package.json").write_text(
        '{"scripts": {"test": "jest"}}',
        encoding="utf-8",
    )

    with patch(
        "backend.app.tools.node_test_runner.subprocess.run",
        side_effect=OSError("Docker unavailable"),
    ):
        result = run_node_tests(str(tmp_path))

    assert result["passed"] is False
    assert result["exit_code"] is None
    assert "Could not start Docker" in result["stderr"]
