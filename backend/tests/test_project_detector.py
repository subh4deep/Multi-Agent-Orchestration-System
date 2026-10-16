
from backend.app.tools.project_detector import detect_project


def test_detects_python_project(tmp_path):
    (tmp_path / "app.py").write_text(
        "def add(a, b):\n    return a + b\n",
        encoding="utf-8",
    )
    (tmp_path / "requirements.txt").write_text(
        "pytest\n",
        encoding="utf-8",
    )
    (tmp_path / "test_app.py").write_text(
        "def test_add():\n    assert 1 + 1 == 2\n",
        encoding="utf-8",
    )

    result = detect_project(str(tmp_path))

    assert result["language"] == "python"
    assert result["test_framework"] == "pytest"
    assert "requirements.txt" in result["dependency_files"]
    assert "test_app.py" in result["test_files"]
    assert result["error"] is None


def test_handles_missing_workspace(tmp_path):
    missing = tmp_path / "missing"

    result = detect_project(str(missing))

    assert result["language"] == "unknown"
    assert result["error"] == "Workspace directory does not exist."


def test_detects_node_project(tmp_path):
    package_file = tmp_path / "package.json"
    package_file.write_text(
        '{"name": "demo", "scripts": {"test": "jest"}}',
        encoding="utf-8",
    )

    result = detect_project(str(tmp_path))

    assert result["language"] == "javascript"
    assert result["test_framework"] == "npm"
    assert "package.json" in result["dependency_files"]
