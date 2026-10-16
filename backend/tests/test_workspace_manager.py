
from pathlib import Path

from backend.app.tools.workspace_manager import (
    create_workspace,
    cleanup_workspace,
)


def test_create_workspace(tmp_path):
    workspace = Path(
        create_workspace({"src/app.py": "print('hello')"})
    )

    try:
        assert (workspace / "src" / "app.py").read_text(
            encoding="utf-8"
        ) == "print('hello')"
    finally:
        cleanup_workspace(str(workspace))

    assert not workspace.exists()


def test_rejects_path_traversal():
    try:
        create_workspace({"../outside.txt": "unsafe"})
        assert False, "Expected ValueError"
    except ValueError:
        pass
