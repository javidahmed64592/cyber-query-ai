"""Unit tests for the cyber_query_ai.main module."""

from cyber_query_ai.main import run


def test_run() -> None:
    """Test the run function."""
    result = run()
    assert result == "This is a run function."
