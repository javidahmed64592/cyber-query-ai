"""Unit tests for the cyber_query_ai.models module."""

from cyber_query_ai.models import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    CodeExplanationResponse,
    CodeGenerationResponse,
    ConfigResponse,
    Exploit,
    ExploitSearchResponse,
    HealthResponse,
    PromptRequest,
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
        version = "x.y.z"
        response = ConfigResponse(model=model, embedding_model=embedding_model, host=host, port=port, version=version)
        expected = {"model": model, "embedding_model": embedding_model, "host": host, "port": port, "version": version}
        assert response.model_dump() == expected


class TestChatResponse:
    """Unit tests for the ChatResponse model."""

    def test_model_dump(self) -> None:
        """Test the model_dump method."""
        message = "This is a response message."
        response = ChatResponse(message=message)
        expected = {"message": message}
        assert response.model_dump() == expected


class TestCodeGenerationResponse:
    """Unit tests for the CodeGenerationResponse model."""

    def test_model_dump_single_line(self) -> None:
        """Test the model_dump method for single-line command."""
        code = "nmap -sn 192.168.1.0/24"
        explanation = "Performs a ping scan of the network"
        language = "bash"
        response = CodeGenerationResponse(code=code, explanation=explanation, language=language)
        expected = {
            "code": code,
            "explanation": explanation,
            "language": language,
        }
        assert response.model_dump() == expected

    def test_model_dump_multi_line(self) -> None:
        """Test the model_dump method for multi-line script."""
        code = "#!/bin/bash\nfor i in $(seq 1 254); do\n  ping -c 1 192.168.1.$i\ndone"
        explanation = "Script that pings all hosts in the network"
        language = "bash"
        response = CodeGenerationResponse(code=code, explanation=explanation, language=language)
        expected = {
            "code": code,
            "explanation": explanation,
            "language": language,
        }
        assert response.model_dump() == expected


class TestCodeExplanationResponse:
    """Unit tests for the CodeExplanationResponse model."""

    def test_model_dump(self) -> None:
        """Test the model_dump method."""
        explanation = "This is an explanation"
        response = CodeExplanationResponse(explanation=explanation)
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
