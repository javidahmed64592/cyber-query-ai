"""Unit tests for the cyber_query_ai.main module."""

from cyber_query_ai.main import example_function


def test_example_function() -> None:
    """Test the example_function."""
    result = example_function()
    assert result == "This is an example function."
