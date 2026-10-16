
from pathlib import Path
import subprocess
from unittest import result

from backend.app.tools.patch_applier import apply_patch
from backend.app.tools.workspace_manager import (
    create_workspace,
    cleanup_workspace,
)


def initialize_git_repository(workspace: str) -> None:
    subprocess.run(
        ["git", "init"],
        cwd=workspace,
        check=True,
        capture_output=True,
        text=True,
    )


def test_applies_valid_patch():
    workspace = create_workspace({"app.py": 'print("old")\n'})

    try:
        initialize_git_repository(workspace)

        subprocess.run(
            ["git", "add", "app.py"],
            cwd=workspace,
            check=True,
            capture_output=True,
            text=True,
        )

        patch = (
            "--- a/app.py\n"
            "+++ b/app.py\n"
            "@@ -1 +1 @@\n"
            '-print("old")\n'
            '+print("new")\n'
        )

        result = apply_patch(workspace, patch)

        print("PATCH RESULT:", result)
        assert result["success"] is True
        assert Path(workspace, "app.py").read_text(
            encoding="utf-8"
        ) == 'print("new")\n'
    finally:
        cleanup_workspace(workspace)


def test_rejects_invalid_patch():
    workspace = create_workspace({"app.py": 'print("old")\n'})

    try:
        initialize_git_repository(workspace)

        subprocess.run(
            ["git", "add", "app.py"],
            cwd=workspace,
            check=True,
            capture_output=True,
            text=True,
        )

        result = apply_patch(workspace, "this is not a valid diff")

        assert result["success"] is False
    finally:
        cleanup_workspace(workspace)
