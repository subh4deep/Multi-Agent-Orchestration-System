
from backend.app.graph.workflow import route_after_execution, MAX_RETRIES


def test_retry_after_failed_tests():
    state = {
        "tests_passed": False,
        "retry_count": 0,
    }

    assert route_after_execution(state) == "retry"


def test_stop_after_retry_limit():
    state = {
        "tests_passed": False,
        "retry_count": MAX_RETRIES,
    }

    assert route_after_execution(state) == "end"


def test_stop_when_tests_pass():
    state = {
        "tests_passed": True,
        "retry_count": 0,
    }

    assert route_after_execution(state) == "end"
