"""Unit tests for the cyber_query_ai.models module."""

from cyber_query_ai.models import CommandGenerationResponse, PromptRequest


class TestPromptRequest:
    """Unit tests for the PromptRequest model."""

    def test_model_dump(self) -> None:
        """Test the model_dump method."""
        prompt = "Generate a command to list all files"
        request = PromptRequest(prompt=prompt)
        expected = {"prompt": prompt}
        assert request.model_dump() == expected


class TestCommandGenerationResponse:
    """Unit tests for the CommandGenerationResponse model."""

    def test_model_dump(self) -> None:
        """Test the model_dump method."""
        commands = ["ls -la", "cat /etc/passwd"]
        explanation = "List all files and show the contents of passwd file."
        response = CommandGenerationResponse(commands=commands, explanation=explanation)
        expected = {
            "commands": commands,
            "explanation": explanation,
        }
        assert response.model_dump() == expected
