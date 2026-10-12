
from backend.app.tools.repository_tools import fetch_repository_files


def test_fetch_repository_files():
    files = fetch_repository_files("subh4deep", "ResumeX")

    assert isinstance(files, dict)
    assert files
    assert all(isinstance(path, str) for path in files)
    assert all(isinstance(content, str) for content in files.values())
