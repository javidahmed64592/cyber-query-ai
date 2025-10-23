"""Unit tests for the cyber_query_ai.models module."""

from cyber_query_ai.models import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    CommandGenerationResponse,
    ConfigResponse,
    ExplanationResponse,
    Exploit,
    ExploitSearchResponse,
    HealthResponse,
    PromptRequest,
    PromptWithLanguageRequest,
    ScriptGenerationResponse,
)


# Request schemas
class TestChatMessage:
    """Unit tests for the ChatMessage model."""

    def test_model_dump(self) -> None:
        """Test the model_dump method."""
        role = "user"
        content = "Hello, how can I help you?"
        message = ChatMessage(role=role, content=content)
        expected = {"role": role, "content": content}
        assert message.model_dump() == expected


class TestChatRequest:
    """Unit tests for the ChatRequest model."""

    def test_model_dump(self) -> None:
        """Test the model_dump method."""
        message = "What is cybersecurity?"
        history = [
            ChatMessage(role="user", content="Hello"),
            ChatMessage(role="assistant", content="Hi! How can I assist you?"),
        ]
        request = ChatRequest(message=message, history=history)
        expected = {
            "message": message,
            "history": [msg.model_dump() for msg in history],
        }
        assert request.model_dump() == expected


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


class TestConfigResponse:
    """Unit tests for the ConfigResponse model."""

    def test_model_dump(self) -> None:
        """Test the model_dump method."""
        model = "mistral"
        embedding_model = "bge-m3"
        host = "localhost"
        port = 8000
        response = ConfigResponse(model=model, embedding_model=embedding_model, host=host, port=port)
        expected = {"model": model, "embedding_model": embedding_model, "host": host, "port": port}
        assert response.model_dump() == expected


class TestChatResponse:
    """Unit tests for the ChatResponse model."""

    def test_model_dump(self) -> None:
        """Test the model_dump method."""
        message = "This is a response message."
        response = ChatResponse(message=message)
        expected = {"message": message}
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
        severity = "high"
        description = "A description"
        exploit = Exploit(title=title, link=link, severity=severity, description=description)
        expected = {"title": title, "link": link, "severity": severity, "description": description}
        assert exploit.model_dump() == expected


class TestExploitSearchResponse:
    """Unit tests for the ExploitSearchResponse model."""

    def test_model_dump(self) -> None:
        """Test the model_dump method."""
        exploits = [
            Exploit(title="Exploit1", link="link1", severity="low", description="desc1"),
            Exploit(title="Exploit2", link="link2", severity="medium", description="desc2"),
        ]
        explanation = "web"
        response = ExploitSearchResponse(exploits=exploits, explanation=explanation)
        expected = {"exploits": [e.model_dump() for e in exploits], "explanation": explanation}
        assert response.model_dump() == expected
