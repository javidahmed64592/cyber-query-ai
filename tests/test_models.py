"""Unit tests for the cyber_query_ai.models module."""

from cyber_query_ai.models import CommandGenerationResponse, PromptRequest


class TestPromptRequest:
    """Unit tests for the PromptRequest model."""

    def test_valid_request(self) -> None:
        """Test a valid PromptRequest."""
        prompt = "Generate a command to list all files"
        request = PromptRequest(prompt=prompt)
        assert request.prompt == prompt


class TestCommandGenerationResponse:
    """Unit tests for the CommandGenerationResponse model."""

    def test_valid_response(self) -> None:
        """Test a valid CommandGenerationResponse."""
        commands = ["ls -la", "cat /etc/passwd"]
        explanation = "List all files and show the contents of passwd file."
        response = CommandGenerationResponse(commands=commands, explanation=explanation)
        assert response.commands == commands
        assert response.explanation == explanation
