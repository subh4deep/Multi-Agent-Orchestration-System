
from backend.app.graph.workflow import route_after_execution


def test_successful_tests_end_workflow():
    state = {
        "tests_passed": True,
        "retry_count": 0,
    }

    assert route_after_execution(state) == "end"


def test_failed_tests_trigger_retry():
    state = {
        "tests_passed": False,
        "retry_count": 0,
    }

    assert route_after_execution(state) == "retry"


def test_workflow_stops_after_max_retries():
    state = {
        "tests_passed": False,
        "retry_count": 2,
    }

    assert route_after_execution(state) == "end"
