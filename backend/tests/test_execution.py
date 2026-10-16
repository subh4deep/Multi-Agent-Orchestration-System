
from backend.app.graph.execution import execute_patch_pipeline


def test_invalid_patch_is_rejected():
    result = execute_patch_pipeline(
        repository_files={"app.py": 'print("hello")\n'},
        patch="not a valid patch",
    )

    assert result["patch_validation"]["valid"] is False
    assert result["patch_application"]["success"] is False
    assert result["test_results"] == []
    assert result["tests_passed"] is False
