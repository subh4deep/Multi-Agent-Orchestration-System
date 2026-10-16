
import subprocess
from pathlib import Path
import os

ALLOWED_TEST_COMMANDS = {
    "pytest": ["python", "-m", "pytest", "-q"],
}


DOCKER_IMAGE = os.getenv(
    "DEVFLOW_DOCKER_IMAGE",
    "devflow-test-runner:latest",
)


def run_tests(
    workspace: str,
    test_command: str = "pytest",
    timeout: int = 60,
) -> dict:
    if test_command not in ALLOWED_TEST_COMMANDS:
        return {
            "passed": False,
            "exit_code": None,
            "stdout": "",
            "stderr": "Test command is not allowed.",
        }

    workspace_path = Path(workspace).resolve()

    if not workspace_path.is_dir():
        return {
            "passed": False,
            "exit_code": None,
            "stdout": "",
            "stderr": "Workspace directory does not exist.",
        }

    command = [
        "docker",
        "run",
        "--rm",
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
        *ALLOWED_TEST_COMMANDS[test_command],
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

    except subprocess.TimeoutExpired as exc:
        return {
            "passed": False,
            "exit_code": None,
            "stdout": exc.stdout or "",
            "stderr": f"Tests timed out after {timeout} seconds.",
        }

    except OSError as exc:
        return {
            "passed": False,
            "exit_code": None,
            "stdout": "",
            "stderr": f"Could not start Docker: {exc}",
        }
