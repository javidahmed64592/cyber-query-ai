"""Unit tests for the cyber_query_ai.models module."""

from cyber_query_ai.models import (
    CommandGenerationResponse,
    ExplanationResponse,
    Exploit,
    ExploitSearchResponse,
    HealthResponse,
    PromptRequest,
    PromptWithLanguageRequest,
    ScriptGenerationResponse,
)


# Request schemas
class TestPromptRequest:
    """Unit tests for the PromptRequest model."""

    def test_model_dump(self) -> None:
        """Test the model_dump method."""
        prompt = "Generate a command to list all files"
        request = PromptRequest(prompt=prompt)
        expected = {"prompt": prompt}
        assert request.model_dump() == expected


class TestPromptWithLanguageRequest:
    """Unit tests for the PromptWithLanguageRequest model."""

    def test_model_dump(self) -> None:
        """Test the model_dump method."""
        prompt = "Generate a command"
        language = "bash"
        request = PromptWithLanguageRequest(prompt=prompt, language=language)
        expected = {"prompt": prompt, "language": language}
        assert request.model_dump() == expected


# Response schemas
class TestHealthResponse:
    """Unit tests for the HealthResponse model."""

    def test_model_dump(self) -> None:
        """Test the model_dump method."""
        status = "ok"
        timestamp = "<timestamp>"
        response = HealthResponse(status=status, timestamp=timestamp)
        expected = {"status": status, "timestamp": timestamp}
        assert response.model_dump() == expected


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


class TestScriptGenerationResponse:
    """Unit tests for the ScriptGenerationResponse model."""

    def test_model_dump(self) -> None:
        """Test the model_dump method."""
        script = "#!/bin/bash\necho hello"
        explanation = "A simple script"
        response = ScriptGenerationResponse(script=script, explanation=explanation)
        expected = {"script": script, "explanation": explanation}
        assert response.model_dump() == expected


class TestExplanationResponse:
    """Unit tests for the ExplanationResponse model."""

    def test_model_dump(self) -> None:
        """Test the model_dump method."""
        explanation = "This is an explanation"
        response = ExplanationResponse(explanation=explanation)
        expected = {"explanation": explanation}
        assert response.model_dump() == expected


class TestExploit:
    """Unit tests for the Exploit model."""

    def test_model_dump(self) -> None:
        """Test the model_dump method."""
        title = "Sample Exploit"
        link = "http://example.com"
        description = "A description"
        severity = "high"
        exploit = Exploit(title=title, link=link, description=description, severity=severity)
        expected = {"title": title, "link": link, "description": description, "severity": severity}
        assert exploit.model_dump() == expected


class TestExploitSearchResponse:
    """Unit tests for the ExploitSearchResponse model."""

    def test_model_dump(self) -> None:
        """Test the model_dump method."""
        attack_vector = "web"
        exploits = [
            Exploit(title="Exploit1", link="link1", description="desc1", severity="low"),
            Exploit(title="Exploit2", link="link2", description="desc2", severity="medium"),
        ]
        response = ExploitSearchResponse(attack_vector=attack_vector, exploits=exploits)
        expected = {"attack_vector": attack_vector, "exploits": [e.model_dump() for e in exploits]}
        assert response.model_dump() == expected
