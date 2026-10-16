
def select_test_command(project_info: dict) -> str | None:
    if project_info.get("error"):
        return None

    language = project_info.get("language")
    framework = project_info.get("test_framework")

    if language == "python" and framework == "pytest":
        return "pytest"

    if language == "javascript" and framework == "npm":
        return "npm"

    return None
