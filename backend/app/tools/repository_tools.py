
from backend.app.tools.github_client import get_github_client


IGNORED_DIRS = {
    ".git",
    ".github",
    ".venv",
    "node_modules",
    "__pycache__",
    "dist",
    "build",
}

MAX_FILES = 100
MAX_FILE_SIZE = 100_000


def fetch_repository_files(
    owner: str,
    repo_name: str,
    branch: str | None = None,
) -> dict[str, str]:
    client = get_github_client()
    repo = client.get_repo(f"{owner}/{repo_name}")

    if branch is None:
        branch = repo.default_branch

    tree = repo.get_git_tree(branch, recursive=True)

    files = {}

    for item in tree.tree:
        if item.type != "blob":
            continue

        parts = item.path.split("/")

        if any(part in IGNORED_DIRS for part in parts):
            continue

        if not item.path.endswith(
            (".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".go", ".rs")
        ):
            continue

        if item.size is None or item.size > MAX_FILE_SIZE:
            continue

        if len(files) >= MAX_FILES:
            break

        try:
            content = repo.get_contents(item.path, ref=branch)

            if isinstance(content, list):
                continue

            files[item.path] = content.decoded_content.decode("utf-8")
        except (UnicodeDecodeError, ValueError):
            continue

    return files
