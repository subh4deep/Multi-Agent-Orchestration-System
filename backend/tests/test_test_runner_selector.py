
from backend.app.tools.test_runner_selector import select_test_command


def test_selects_pytest():
    assert select_test_command({
        "language": "python",
        "test_framework": "pytest",
        "error": None,
    }) == "pytest"


def test_selects_npm():
    assert select_test_command({
        "language": "javascript",
        "test_framework": "npm",
        "error": None,
    }) == "npm"


def test_rejects_unsupported_project():
    assert select_test_command({
        "language": "unknown",
        "test_framework": None,
        "error": None,
    }) is None


def test_rejects_project_detection_error():
    assert select_test_command({
        "language": "python",
        "test_framework": "pytest",
        "error": "Workspace directory does not exist.",
    }) is None
