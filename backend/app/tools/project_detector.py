
from pathlib import Path


def detect_project(workspace: str) -> dict:
    root = Path(workspace).resolve()

    if not root.is_dir():
        return {
            "language": "unknown",
            "test_framework": None,
            "dependency_files": [],
            "test_files": [],
            "error": "Workspace directory does not exist.",
        }

    ignored = {
        ".git",
        ".venv",
        "venv",
        "node_modules",
        "__pycache__",
    }

    files = [
        path
        for path in root.rglob("*")
        if path.is_file()
        and not any(
            part in ignored
            for part in path.relative_to(root).parts
        )
    ]

    relative_paths = [
        path.relative_to(root).as_posix()
        for path in files
    ]

    filenames = {Path(path).name for path in relative_paths}

    python_dependencies = {
        "requirements.txt",
        "pyproject.toml",
        "Pipfile",
        "setup.py",
    }

    dependency_files = sorted(
        path
        for path in relative_paths
        if Path(path).name in python_dependencies
        or Path(path).name == "package.json"
        or Path(path).name == "package-lock.json"
    )

    python_tests = sorted(
        path
        for path in relative_paths
        if Path(path).suffix == ".py"
        and (
            Path(path).name.startswith("test_")
            or Path(path).name.endswith("_test.py")
        )
    )

    has_python = any(
        Path(path).suffix == ".py"
        for path in relative_paths
    )
    has_node = "package.json" in filenames

    if has_python:
        language = "python"
        test_files = python_tests
        framework = "pytest" if python_tests else None
    elif has_node:
        language = "javascript"
        test_files = [
            path
            for path in relative_paths
            if Path(path).name.endswith(
                (".test.js", ".spec.js", ".test.ts", ".spec.ts")
            )
        ]
        framework = (
            "npm"
            if "package.json" in filenames
            else None
        )
    else:
        language = "unknown"
        test_files = []
        framework = None

    return {
        "language": language,
        "test_framework": framework,
        "dependency_files": dependency_files,
        "test_files": test_files,
        "error": None,
    }
