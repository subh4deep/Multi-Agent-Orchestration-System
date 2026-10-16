
import os
import subprocess
from pathlib import Path


DOCKER_IMAGE = os.getenv(
    "DEVFLOW_NODE_DOCKER_IMAGE",
    "devflow-node-test-runner:latest",
)


def run_node_tests(
    workspace: str,
    timeout: int = 60,
) -> dict:
    workspace_path = Path(workspace).resolve()

    if not workspace_path.is_dir():
        return {
            "passed": False,
            "exit_code": None,
            "stdout": "",
            "stderr": "Workspace directory does not exist.",
        }

    package_file = workspace_path / "package.json"

    if not package_file.is_file():
        return {
            "passed": False,
            "exit_code": None,
            "stdout": "",
            "stderr": "package.json not found.",
        }

    command = [
        "docker", "run", "--rm",
        "--network", "none",
        "--memory", "512m",
        "--cpus", "1",
        "--pids-limit", "128",
        "--read-only",
        "--tmpfs", "/tmp:rw,noexec,nosuid,size=64m",
        "--mount",
        f"type=bind,source={workspace_path},target=/workspace,readonly",
        "--workdir", "/workspace",
        DOCKER_IMAGE,
        "npm", "test", "--", "--run",
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
        )

        return {
            "passed": result.returncode == 0,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    except subprocess.TimeoutExpired:
        return {
            "passed": False,
            "exit_code": None,
            "stdout": "",
            "stderr": f"Node.js tests timed out after {timeout} seconds.",
        }

    except OSError as exc:
        return {
            "passed": False,
            "exit_code": None,
            "stdout": "",
            "stderr": f"Could not start Docker: {exc}",
        }
