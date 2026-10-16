
import subprocess
from pathlib import Path


def apply_patch(workspace: str, patch: str) -> dict:
    workspace_path = Path(workspace).resolve()

    if not workspace_path.is_dir():
        return {"success": False, "error": "Workspace does not exist."}

    try:
        check_result = subprocess.run(
            ["git", "apply", "--check", "-"],
            input=patch,
            cwd=workspace_path,
            capture_output=True,
            text=True,
            shell=False,
            timeout=15,
        )

        if check_result.returncode != 0:
            return {
                "success": False,
                "error": check_result.stderr.strip()
                or "Patch validation failed.",
            }

        result = subprocess.run(
            ["git", "apply", "-"],
            input=patch,
            cwd=workspace_path,
            capture_output=True,
            text=True,
            shell=False,
            timeout=15,
        )

        if result.returncode != 0:
            return {
                "success": False,
                "error": result.stderr.strip()
                or "Patch application failed.",
            }

        return {"success": True, "error": None}

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Git patch operation timed out.",
        }
