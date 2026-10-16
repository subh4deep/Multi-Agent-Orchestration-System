
import shutil
import tempfile
from pathlib import Path


def create_workspace(repository_files: dict[str, str]) -> str:
    workspace = Path(tempfile.mkdtemp(prefix="devflow-"))

    try:
        for relative_path, content in repository_files.items():
            file_path = Path(relative_path)

            if file_path.is_absolute() or ".." in file_path.parts:
                raise ValueError(f"Unsafe repository path: {relative_path}")

            destination = (workspace / file_path).resolve()

            if not destination.is_relative_to(workspace.resolve()):
                raise ValueError(f"Unsafe repository path: {relative_path}")

            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8")

        return str(workspace)

    except Exception:
        shutil.rmtree(workspace, ignore_errors=True)
        raise


def cleanup_workspace(workspace: str) -> None:
    shutil.rmtree(workspace, ignore_errors=True)
