
from pathlib import Path

from backend.app.tools.test_runner import run_tests


def test_runs_pytest_inside_docker(tmp_path: Path):
    test_file = tmp_path / "test_example.py"
    test_file.write_text(
        "def test_addition():\n"
        "    assert 1 + 1 == 2\n",
        encoding="utf-8",
    )

    result = run_tests(str(tmp_path))

    assert result["passed"] is True, result
    assert result["exit_code"] == 0
    assert "1 passed" in result["stdout"]


def test_rejects_unknown_test_command(tmp_path: Path):
    result = run_tests(str(tmp_path), test_command="powershell")

    assert result["passed"] is False
    assert result["exit_code"] is None
    assert result["stderr"] == "Test command is not allowed."
