
import re


def validate_patch(patch: str, repository_files: dict[str, str]) -> dict:
    if not patch or not patch.strip():
        return {
            "valid": False,
            "error": "Generated patch is empty.",
        }

    if "```" in patch:
        return {
            "valid": False,
            "error": "Patch contains Markdown code fences.",
        }

    file_headers = re.findall(r"^\+\+\+ b/(.+)$", patch, re.MULTILINE)

    if not file_headers:
        return {
            "valid": False,
            "error": "No valid unified diff file headers found.",
        }

    allowed_files = set(repository_files)

    for path in file_headers:
        if path not in allowed_files:
            return {
                "valid": False,
                "error": f"Patch targets an unknown file: {path}",
            }

        if path.startswith("/") or ".." in path.split("/"):
            return {
                "valid": False,
                "error": f"Unsafe file path: {path}",
            }

    if not re.search(r"^@@ ", patch, re.MULTILINE):
        return {
            "valid": False,
            "error": "Patch contains no unified diff hunks.",
        }

    return {
        "valid": True,
        "files": file_headers,
        "error": None,
    }
