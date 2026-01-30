"""Unit tests for the cyber_query_ai.server module."""

import asyncio
import json
from collections.abc import Generator
from importlib.metadata import PackageMetadata
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException, Request, Security
from fastapi.routing import APIRoute
from fastapi.security import APIKeyHeader
from fastapi.testclient import TestClient
from python_template_server.models import ResponseCode

from cyber_query_ai.chatbot import Chatbot
from cyber_query_ai.models import (
    ChatMessageModel,
    CyberQueryAIConfig,
    PostChatRequest,
    PostChatResponse,
    PostCodeExplanationResponse,
    PostCodeGenerationResponse,
    PostExploitSearchResponse,
    PostPromptRequest,
    RoleType,
)
from cyber_query_ai.server import CyberQueryAIServer


@pytest.fixture(autouse=True)
def mock_package_metadata() -> Generator[MagicMock]:
    """Mock importlib.metadata.metadata to return a mock PackageMetadata."""
    with patch("python_template_server.template_server.metadata") as mock_metadata:
        mock_pkg_metadata = MagicMock(spec=PackageMetadata)
        metadata_dict = {
            "Name": "cyber-query-ai",
            "Version": "0.1.0",
            "Summary": "AI-powered cybersecurity assistant",
        }
        mock_pkg_metadata.__getitem__.side_effect = lambda key: metadata_dict[key]
        mock_metadata.return_value = mock_pkg_metadata
        yield mock_metadata


@pytest.fixture
def mock_chatbot(
    mock_post_chat_response: PostChatResponse,
    mock_post_code_generation_response: PostCodeGenerationResponse,
    mock_post_code_explanation_response: PostCodeExplanationResponse,
    mock_post_exploit_search_response: PostExploitSearchResponse,
) -> MagicMock:
    """Provide a mock Chatbot instance."""
    mock = MagicMock(spec=Chatbot)
    mock.llm = MagicMock(autospec=True)
    mock.llm.invoke = MagicMock(return_value="Mock LLM response")
    mock.prompt_chat = MagicMock(return_value=str(mock_post_chat_response.model_dump()))
    mock.prompt_code_generation = MagicMock(return_value=str(mock_post_code_generation_response.model_dump()))
    mock.prompt_code_explanation = MagicMock(return_value=str(mock_post_code_explanation_response.model_dump()))
    mock.prompt_exploit_search = MagicMock(return_value=str(mock_post_exploit_search_response.model_dump()))
    return mock


@pytest.fixture
def mock_server(
    mock_cyber_query_ai_config: CyberQueryAIConfig,
    mock_chatbot: MagicMock,
) -> Generator[CyberQueryAIServer]:
    """Provide a CyberQueryAIServer instance for testing."""

    async def fake_verify_api_key(
        api_key: str | None = Security(APIKeyHeader(name="X-API-Key", auto_error=False)),
    ) -> None:
        """Fake verify API key that accepts the security header and always succeeds in tests."""
        return

    with (
        patch.object(CyberQueryAIServer, "_verify_api_key", new=fake_verify_api_key),
        patch("cyber_query_ai.server.Chatbot", return_value=mock_chatbot),
        patch("cyber_query_ai.server.CyberQueryAIConfig.save_to_file"),
    ):
        server = CyberQueryAIServer(mock_cyber_query_ai_config)
        yield server


class TestCyberQueryAIServer:
    """Unit tests for the CyberQueryAIServer class."""

    def test_init(self, mock_server: CyberQueryAIServer) -> None:
        """Test CyberQueryAIServer initialization."""
        assert isinstance(mock_server.config, CyberQueryAIConfig)
        assert isinstance(mock_server.chatbot, Chatbot)
        assert isinstance(mock_server.static_dir, Path)

    def test_parse_response(self, mock_server: CyberQueryAIServer, mock_post_chat_response: PostChatResponse) -> None:
        """Test parsing JSON response strings."""
        response_str = json.dumps(mock_post_chat_response.model_dump())
        parsed = mock_server.parse_response(response_str)
        assert parsed == mock_post_chat_response.model_dump()

    def test_validate_keys(self, mock_server: CyberQueryAIServer) -> None:
        """Test validation of required keys in response dictionary."""
        required_keys = {"key1", "key2", "key3"}
        response_dict = {"key1": "value1", "key2": "value2"}
        with pytest.raises(KeyError):
            mock_server.validate_keys(required_keys, response_dict)

    def test_validate_config(
        self, mock_server: CyberQueryAIServer, mock_cyber_query_ai_config: CyberQueryAIConfig
    ) -> None:
        """Test configuration validation."""
        config_dict = mock_cyber_query_ai_config.model_dump()
        validated_config = mock_server.validate_config(config_dict)
        assert validated_config == mock_cyber_query_ai_config

    def test_validate_config_invalid_returns_default(self, mock_server: CyberQueryAIServer) -> None:
        """Test invalid configuration returns default configuration."""
        invalid_config = {"model": None}
        validated_config = mock_server.validate_config(invalid_config)
        assert isinstance(validated_config, CyberQueryAIConfig)


class TestCyberQueryAIServerRoutes:
    """Integration tests for the routes in CyberQueryAIServer."""

    def test_setup_routes(self, mock_server: CyberQueryAIServer) -> None:
        """Test that routes are set up correctly."""
        api_routes = [route for route in mock_server.app.routes if isinstance(route, APIRoute)]
        routes = [route.path for route in api_routes]
        expected_endpoints = [
            "/health",
            "/login",
            "/config",
            "/model/chat",
            "/code/generate",
            "/code/explain",
            "/exploit/search",
        ]
        for endpoint in expected_endpoints:
            assert endpoint in routes, f"Expected endpoint {endpoint} not found in routes"


class TestGetApiConfigEndpoint:
    """Integration tests for the /config endpoint."""

    @pytest.fixture
    def mock_request_object(self) -> MagicMock:
        """Provide a mock Request object with JSON data."""
        return MagicMock(spec=Request)

    def test_get_api_config(self, mock_server: CyberQueryAIServer, mock_request_object: MagicMock) -> None:
        """Test the /config endpoint method."""
        response = asyncio.run(mock_server.get_api_config(mock_request_object))

        assert response.message == "Successfully retrieved chatbot configuration."
        assert isinstance(response.timestamp, str)
        assert response.model == mock_server.config.model
        assert response.version == mock_server.package_metadata["Version"]

    def test_get_api_config_endpoint(self, mock_server: CyberQueryAIServer) -> None:
        """Test /config endpoint returns 200."""
        app = mock_server.app
        client = TestClient(app)

        response = client.get("/config")
        assert response.status_code == ResponseCode.OK

        assert response.content, "Response body is empty"
        response_body = response.json()
        assert response_body["message"] == "Successfully retrieved chatbot configuration."
        assert isinstance(response_body["timestamp"], str)
        assert response_body["model"] == mock_server.config.model.model_dump()
        assert response_body["version"] == mock_server.package_metadata["Version"]


class TestPostChatEndpoint:
    """Integration and unit tests for the /model/chat endpoint."""

    @pytest.fixture
    def mock_request_body(self) -> PostChatRequest:
        """Provide a mock request body for system metrics history."""
        return PostChatRequest(
            message="What is cybersecurity?", history=[ChatMessageModel(role=RoleType.USER, content="Hello")]
        )

    @pytest.fixture
    def mock_request_object(self, mock_request_body: PostChatRequest) -> MagicMock:
        """Provide a mock Request object with JSON data."""
        request = MagicMock(spec=Request)
        request.json = AsyncMock(return_value=mock_request_body.model_dump())
        return request

    def test_post_chat(
        self,
        mock_server: CyberQueryAIServer,
        mock_chatbot: MagicMock,
        mock_request_object: MagicMock,
    ) -> None:
        """Test the /model/chat method handles valid JSON and returns a model reply."""
        mock_response = MagicMock()
        mock_response.content = json.dumps({"model_message": "Cybersecurity is the practice of protecting systems..."})
        mock_chatbot.llm.invoke.return_value = mock_response
        response = asyncio.run(mock_server.post_chat(mock_request_object))

        assert response.message == "Successfully generated chat response."
        assert isinstance(response.timestamp, str)
        assert isinstance(response.model_message, str)

    def test_post_chat_invalid_json(
        self,
        mock_server: CyberQueryAIServer,
        mock_chatbot: MagicMock,
        mock_request_object: MagicMock,
    ) -> None:
        """Test /model/chat handles invalid JSON response from LLM."""
        mock_response = MagicMock()
        mock_response.content = "Not valid JSON"
        mock_chatbot.llm.invoke.return_value = mock_response

        with pytest.raises(HTTPException, match="Invalid JSON response from LLM: Not valid JSON"):
            asyncio.run(mock_server.post_chat(mock_request_object))

    def test_post_chat_missing_keys(
        self,
        mock_server: CyberQueryAIServer,
        mock_chatbot: MagicMock,
        mock_request_object: MagicMock,
    ) -> None:
        """Test /model/chat handles missing keys in LLM response."""
        mock_response = MagicMock()
        mock_response.content = json.dumps({"msg": "Missing model_message key"})
        mock_chatbot.llm.invoke.return_value = mock_response

        with pytest.raises(HTTPException, match=r"LLM response missing required keys."):
            asyncio.run(mock_server.post_chat(mock_request_object))

    def test_post_chat_error(
        self,
        mock_server: CyberQueryAIServer,
        mock_chatbot: MagicMock,
        mock_request_object: MagicMock,
    ) -> None:
        """Test /model/chat handles errors gracefully."""
        mock_chatbot.llm.invoke.side_effect = Exception("LLM error")

        with pytest.raises(HTTPException, match=r"An unexpected error occurred during chat."):
            asyncio.run(mock_server.post_chat(mock_request_object))

    def test_post_chat_endpoint(
        self,
        mock_server: CyberQueryAIServer,
        mock_chatbot: MagicMock,
        mock_request_body: PostChatRequest,
    ) -> None:
        """Test /model/chat endpoint returns 200 and includes reply."""
        app = mock_server.app
        client = TestClient(app)

        mock_response = MagicMock()
        mock_response.content = json.dumps({"model_message": "Cybersecurity is important!"})
        mock_chatbot.llm.invoke.return_value = mock_response
        response = client.post(
            "/model/chat",
            json=mock_request_body.model_dump(),
        )
        assert response.status_code == ResponseCode.OK

        response_body = response.json()
        assert response_body["message"] == "Successfully generated chat response."
        assert isinstance(response_body["timestamp"], str)
        assert isinstance(response_body["model_message"], str)


class TestPostGenerateCodeEndpoint:
    """Integration and unit tests for the /code/generate endpoint."""

    @pytest.fixture
    def mock_request_body(self) -> PostPromptRequest:
        """Provide a mock request body for code generation."""
        return PostPromptRequest(prompt="Generate a command to list files")

    @pytest.fixture
    def mock_request_object(self, mock_request_body: PostPromptRequest) -> MagicMock:
        """Provide a mock Request object with JSON data."""
        request = MagicMock(spec=Request)
        request.json = AsyncMock(return_value=mock_request_body.model_dump())
        return request

    def test_post_generate_code(
        self, mock_server: CyberQueryAIServer, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test the /code/generate method handles valid JSON and returns generated code."""
        mock_response = MagicMock()
        mock_response.content = json.dumps(
            {
                "generated_code": "ls -la",
                "explanation": "Lists all files in long format",
                "language": "bash",
            }
        )
        mock_chatbot.llm.invoke.return_value = mock_response
        response = asyncio.run(mock_server.post_generate_code(mock_request_object))

        assert response.message == "Successfully generated code."
        assert isinstance(response.timestamp, str)
        assert response.generated_code == "ls -la"
        assert response.explanation == "Lists all files in long format"
        assert response.language == "bash"

    def test_post_generate_code_invalid_json(
        self, mock_server: CyberQueryAIServer, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test /code/generate handles invalid JSON response from LLM."""
        mock_response = MagicMock()
        mock_response.content = "Not valid JSON"
        mock_chatbot.llm.invoke.return_value = mock_response

        with pytest.raises(HTTPException, match="Invalid JSON response"):
            asyncio.run(mock_server.post_generate_code(mock_request_object))

    def test_post_generate_code_missing_keys(
        self, mock_server: CyberQueryAIServer, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test /code/generate handles missing keys in LLM response."""
        mock_response = MagicMock()
        mock_response.content = json.dumps({"code": "ls"})
        mock_chatbot.llm.invoke.return_value = mock_response

        with pytest.raises(HTTPException, match="LLM response missing required keys"):
            asyncio.run(mock_server.post_generate_code(mock_request_object))

    def test_post_generate_code_error(
        self, mock_server: CyberQueryAIServer, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test /code/generate handles errors gracefully."""
        mock_chatbot.llm.invoke.side_effect = Exception("LLM error")

        with pytest.raises(HTTPException, match="An unexpected error occurred during code generation"):
            asyncio.run(mock_server.post_generate_code(mock_request_object))

    def test_post_generate_code_endpoint(
        self, mock_server: CyberQueryAIServer, mock_chatbot: MagicMock, mock_request_body: PostPromptRequest
    ) -> None:
        """Test /code/generate endpoint returns 200 and includes code."""
        app = mock_server.app
        client = TestClient(app)

        mock_response = MagicMock()
        mock_response.content = json.dumps(
            {
                "generated_code": "nmap -sn 192.168.1.0/24",
                "explanation": "Scans the network",
                "language": "bash",
            }
        )
        mock_chatbot.llm.invoke.return_value = mock_response
        response = client.post("/code/generate", json=mock_request_body.model_dump())
        assert response.status_code == ResponseCode.OK

        response_body = response.json()
        assert response_body["message"] == "Successfully generated code."
        assert isinstance(response_body["timestamp"], str)
        assert response_body["generated_code"] == "nmap -sn 192.168.1.0/24"


class TestPostExplainCodeEndpoint:
    """Integration and unit tests for the /code/explain endpoint."""

    @pytest.fixture
    def mock_request_body(self) -> PostPromptRequest:
        """Provide a mock request body for code explanation."""
        return PostPromptRequest(prompt="Explain: nmap -sS 192.168.1.1")

    @pytest.fixture
    def mock_request_object(self, mock_request_body: PostPromptRequest) -> MagicMock:
        """Provide a mock Request object with JSON data."""
        request = MagicMock(spec=Request)
        request.json = AsyncMock(return_value=mock_request_body.model_dump())
        return request

    def test_post_explain_code(
        self, mock_server: CyberQueryAIServer, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test the /code/explain method handles valid JSON and returns explanation."""
        mock_response = MagicMock()
        mock_response.content = json.dumps(
            {
                "explanation": "This performs a TCP SYN scan on the target",
            }
        )
        mock_chatbot.llm.invoke.return_value = mock_response
        response = asyncio.run(mock_server.post_explain_code(mock_request_object))

        assert response.message == "Successfully explained code."
        assert isinstance(response.timestamp, str)
        assert response.explanation == "This performs a TCP SYN scan on the target"

    def test_post_explain_code_invalid_json(
        self, mock_server: CyberQueryAIServer, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test /code/explain handles invalid JSON response from LLM."""
        mock_response = MagicMock()
        mock_response.content = "Not valid JSON"
        mock_chatbot.llm.invoke.return_value = mock_response

        with pytest.raises(HTTPException, match="Invalid JSON response"):
            asyncio.run(mock_server.post_explain_code(mock_request_object))

    def test_post_explain_code_missing_keys(
        self, mock_server: CyberQueryAIServer, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test /code/explain handles missing keys in LLM response."""
        mock_response = MagicMock()
        mock_response.content = json.dumps({})
        mock_chatbot.llm.invoke.return_value = mock_response

        with pytest.raises(HTTPException, match="LLM response missing required keys"):
            asyncio.run(mock_server.post_explain_code(mock_request_object))

    def test_post_explain_code_error(
        self, mock_server: CyberQueryAIServer, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test /code/explain handles errors gracefully."""
        mock_chatbot.llm.invoke.side_effect = Exception("LLM error")

        with pytest.raises(HTTPException, match="An unexpected error occurred during code explanation"):
            asyncio.run(mock_server.post_explain_code(mock_request_object))

    def test_post_explain_code_endpoint(
        self, mock_server: CyberQueryAIServer, mock_chatbot: MagicMock, mock_request_body: PostPromptRequest
    ) -> None:
        """Test /code/explain endpoint returns 200 and includes explanation."""
        app = mock_server.app
        client = TestClient(app)

        mock_response = MagicMock()
        mock_response.content = json.dumps(
            {
                "explanation": "This command scans for open ports",
            }
        )
        mock_chatbot.llm.invoke.return_value = mock_response
        response = client.post("/code/explain", json=mock_request_body.model_dump())
        assert response.status_code == ResponseCode.OK

        response_body = response.json()
        assert response_body["message"] == "Successfully explained code."
        assert isinstance(response_body["timestamp"], str)
        assert response_body["explanation"] == "This command scans for open ports"


class TestPostExploitSearchEndpoint:
    """Integration and unit tests for the /exploit/search endpoint."""

    @pytest.fixture
    def mock_request_body(self) -> PostPromptRequest:
        """Provide a mock request body for exploit search."""
        return PostPromptRequest(prompt="Search for Apache exploits")

    @pytest.fixture
    def mock_request_object(self, mock_request_body: PostPromptRequest) -> MagicMock:
        """Provide a mock Request object with JSON data."""
        request = MagicMock(spec=Request)
        request.json = AsyncMock(return_value=mock_request_body.model_dump())
        return request

    def test_post_exploit_search(
        self, mock_server: CyberQueryAIServer, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test the /exploit/search method handles valid JSON and returns exploits."""
        mock_response = MagicMock()
        mock_response.content = json.dumps(
            {
                "exploits": [
                    {
                        "title": "Apache HTTP Server CVE-2021-41773",
                        "link": "https://example.com/cve",
                        "severity": "Critical",
                        "description": "Path traversal vulnerability",
                    }
                ],
                "explanation": "Found 1 exploit for Apache",
            }
        )
        mock_chatbot.llm.invoke.return_value = mock_response
        response = asyncio.run(mock_server.post_exploit_search(mock_request_object))

        assert response.message == "Successfully searched for exploits."
        assert isinstance(response.timestamp, str)
        assert len(response.exploits) == 1
        assert response.exploits[0].title == "Apache HTTP Server CVE-2021-41773"
        assert response.explanation == "Found 1 exploit for Apache"

    def test_post_exploit_search_invalid_json(
        self, mock_server: CyberQueryAIServer, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test /exploit/search handles invalid JSON response from LLM."""
        mock_response = MagicMock()
        mock_response.content = "Not valid JSON"
        mock_chatbot.llm.invoke.return_value = mock_response

        with pytest.raises(HTTPException, match="Invalid JSON response"):
            asyncio.run(mock_server.post_exploit_search(mock_request_object))

    def test_post_exploit_search_missing_keys(
        self, mock_server: CyberQueryAIServer, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test /exploit/search handles missing keys in LLM response."""
        mock_response = MagicMock()
        mock_response.content = json.dumps({"explan": "Missing keys"})
        mock_chatbot.llm.invoke.return_value = mock_response

        with pytest.raises(HTTPException, match="LLM response missing required keys"):
            asyncio.run(mock_server.post_exploit_search(mock_request_object))

    def test_post_exploit_search_error(
        self, mock_server: CyberQueryAIServer, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test /exploit/search handles errors gracefully."""
        mock_chatbot.llm.invoke.side_effect = Exception("LLM error")

        with pytest.raises(HTTPException, match="An unexpected error occurred during exploit search"):
            asyncio.run(mock_server.post_exploit_search(mock_request_object))

    def test_post_exploit_search_endpoint(
        self, mock_server: CyberQueryAIServer, mock_chatbot: MagicMock, mock_request_body: PostPromptRequest
    ) -> None:
        """Test /exploit/search endpoint returns 200 and includes exploits."""
        app = mock_server.app
        client = TestClient(app)

        mock_response = MagicMock()
        mock_response.content = json.dumps(
            {
                "exploits": [
                    {
                        "title": "Test Exploit",
                        "link": "https://example.com",
                        "severity": "High",
                        "description": "Test description",
                    }
                ],
                "explanation": "Found exploits",
            }
        )
        mock_chatbot.llm.invoke.return_value = mock_response
        response = client.post("/exploit/search", json=mock_request_body.model_dump())
        assert response.status_code == ResponseCode.OK

        response_body = response.json()
        assert response_body["message"] == "Successfully searched for exploits."
        assert isinstance(response_body["timestamp"], str)
        assert len(response_body["exploits"]) == 1
