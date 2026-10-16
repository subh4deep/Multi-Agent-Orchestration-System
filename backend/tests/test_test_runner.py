import subprocess

from backend.app.tools.test_runner import run_tests

from unittest.mock import patch, MagicMock

from backend.app.tools.test_runner import run_tests

def test_rejects_unknown_test_command(tmp_path):
    result = run_tests(str(tmp_path), "delete_everything")

    assert result["passed"] is False
    assert result["stderr"] == "Test command is not allowed."


def test_rejects_missing_workspace(tmp_path):
    missing_path = tmp_path / "missing"

    result = run_tests(str(missing_path))

    assert result["passed"] is False
    assert result["stderr"] == "Workspace directory does not exist."


def test_runs_pytest(tmp_path):
    (tmp_path / "test_sample.py").write_text(
        "def test_example():\n    assert 1 + 1 == 2\n",
        encoding="utf-8",
    )

    result = run_tests(str(tmp_path))

    print("RESULT:", result)

    assert result["passed"] is True
    assert result["exit_code"] == 0



def test_returns_failure_when_docker_times_out(tmp_path):
    with patch(
        "backend.app.tools.test_runner.subprocess.run",
        side_effect=__import__("subprocess").TimeoutExpired(
            cmd="docker run",
            timeout=1,
            output="",
            stderr="",
        ),
    ):
        result = run_tests(str(tmp_path), timeout=1)

    assert result["passed"] is False
    assert result["exit_code"] is None
    assert "timed out" in result["stderr"].lower()

def test_handles_docker_not_available(tmp_path):
    with patch(
        "backend.app.tools.test_runner.subprocess.run",
        side_effect=FileNotFoundError("docker executable not found"),
    ):
        result = run_tests(str(tmp_path))

    assert result["passed"] is False
    assert result["exit_code"] is None
    assert "could not start docker" in result["stderr"].lower()