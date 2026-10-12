
from backend.app.tools.patch_validator import validate_patch


def test_valid_patch():
    patch = """--- a/app.py
+++ b/app.py
@@ -1,1 +1,1 @@
-print("old")
+print("new")
"""
    result = validate_patch(patch, {"app.py": 'print("old")'})

    assert result["valid"] is True
    assert result["files"] == ["app.py"]


def test_reject_unknown_file():
    patch = """--- a/unknown.py
+++ b/unknown.py
@@ -1,1 +1,1 @@
-old
+new
"""
    result = validate_patch(patch, {"app.py": "old"})

    assert result["valid"] is False


def test_reject_empty_patch():
    result = validate_patch("", {"app.py": "print('hello')"})

    assert result["valid"] is False
