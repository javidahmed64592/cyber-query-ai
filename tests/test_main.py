"""Unit tests for the cyber_query_ai.main module."""

import json
from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from cyber_query_ai.config import Config
from cyber_query_ai.main import api_router, clean_json_response, create_app, generate_command, run
from cyber_query_ai.models import CommandGenerationResponse, PromptRequest

HTTP_OK = 200
HTTP_UNPROCESSABLE_ENTITY = 422
HTTP_INTERNAL_SERVER_ERROR = 500


@pytest.fixture
def mock_config() -> Config:
    """Fixture for a mock configuration."""
    return Config(model="test-model", host="localhost", port=8000)


@pytest.fixture
def mock_chatbot() -> Generator[MagicMock, None, None]:
    """Fixture to create a mock Chatbot class."""
    with patch("cyber_query_ai.main.Chatbot", autospec=True) as mock:
        chatbot_instance = mock.return_value
        chatbot_instance.prompt_command_generation.return_value = "formatted prompt"
        chatbot_instance.llm = MagicMock()
        yield mock


@pytest.fixture
def mock_run_in_threadpool() -> Generator[MagicMock, None, None]:
    """Fixture to mock the run_in_threadpool function."""
    with patch("cyber_query_ai.main.run_in_threadpool") as mock:
        yield mock


@pytest.fixture
def mock_uvicorn_run() -> Generator[MagicMock, None, None]:
    """Fixture to mock uvicorn.run function."""
    with patch("cyber_query_ai.main.uvicorn.run") as mock:
        yield mock


@pytest.fixture
def mock_load_config() -> Generator[MagicMock, None, None]:
    """Fixture to mock load_config function."""
    with patch("cyber_query_ai.main.load_config") as mock:
        yield mock


@pytest.fixture
def mock_create_app() -> Generator[MagicMock, None, None]:
    """Fixture to mock create_app function."""
    with patch("cyber_query_ai.main.create_app") as mock:
        yield mock


@pytest.fixture
def test_app(mock_config: Config) -> TestClient:
    """Fixture to create a test FastAPI app."""
    app = create_app(mock_config)
    app.include_router(api_router)
    return TestClient(app)


class TestCreateApp:
    """Unit tests for the create_app function."""

    def test_create_app_configuration(self, mock_config: Config, mock_chatbot: MagicMock) -> None:
        """Test that create_app properly configures the FastAPI application."""
        app = create_app(mock_config)

        mock_chatbot.assert_called_once_with(model=mock_config.model)
        assert app.state.chatbot == mock_chatbot.return_value

    def test_create_app_cors_settings(self, mock_config: Config, mock_chatbot: MagicMock) -> None:
        """Test that CORS middleware is configured with proper settings."""
        app = create_app(mock_config)

        cors_middleware = None
        for middleware in app.user_middleware:
            if hasattr(middleware.cls, "__name__") and middleware.cls.__name__ == "CORSMiddleware":
                cors_middleware = middleware
                break

        assert cors_middleware is not None
        assert cors_middleware.kwargs["allow_origins"] == ["*"]
        assert cors_middleware.kwargs["allow_credentials"] is True
        assert cors_middleware.kwargs["allow_methods"] == ["*"]
        assert cors_middleware.kwargs["allow_headers"] == ["*"]


class TestCleanJsonResponse:
    """Unit tests for the clean_json_response function."""

    @pytest.mark.parametrize(
        ("input_json", "expected", "test_description"),
        [
            # Test trailing commas removal
            (
                '{"commands": ["nmap -sS target",], "explanation": "test",}',
                '{"commands": ["nmap -sS target"], "explanation": "test"}',
                "removes trailing commas from arrays and objects",
            ),
            # Test markdown blocks removal
            (
                '```json\n{"commands": ["ls"], "explanation": "list files"}\n```',
                '{"commands": ["ls"], "explanation": "list files"}',
                "removes markdown code blocks",
            ),
            # Test structural issues fix
            (
                '{"commands": ["nmap -sS target", "explanation": "SYN scan"]}',
                '{"commands": ["nmap -sS target"], "explanation": "SYN scan"}',
                "fixes structural issues with explanation inside commands array",
            ),
            # Test whitespace stripping
            (
                '  \n{"commands": ["ls"], "explanation": "test"}  \n',
                '{"commands": ["ls"], "explanation": "test"}',
                "strips leading and trailing whitespace",
            ),
            # Test combined issues
            (
                '```json\n{"commands": ["nmap", "explanation": "scan",], "extra": "data",}\n```',
                '{"commands": ["nmap"], "explanation": "scan", "extra": "data"}',
                "fixes multiple issues simultaneously",
            ),
            # Test valid JSON unchanged
            (
                '{"commands": ["ls"], "explanation": "test"}',
                '{"commands": ["ls"], "explanation": "test"}',
                "leaves valid JSON unchanged except for whitespace",
            ),
        ],
    )
    def test_clean_json_response(self, input_json: str, expected: str, test_description: str) -> None:
        """Test that clean_json_response function handles various JSON formatting issues."""
        result = clean_json_response(input_json)
        assert result == expected, f"Failed to {test_description}"


class TestGenerateCommand:
    """Unit tests for the generate_command endpoint."""

    @pytest.fixture
    def mock_request(self, test_app: TestClient) -> MagicMock:
        """Fixture to create a mock FastAPI Request object."""
        mock_req = MagicMock()
        mock_req.app.state.chatbot = test_app.app.state.chatbot  # type: ignore[attr-defined]
        return mock_req

    @pytest.mark.asyncio
    async def test_generate_command_success(
        self, mock_run_in_threadpool: MagicMock, mock_request: MagicMock, mock_chatbot: MagicMock
    ) -> None:
        """Test successful command generation."""
        prompt_request = PromptRequest(prompt="scan for open ports")
        mock_response = {
            "commands": ["nmap -sS -O target"],
            "explanation": "Perform a SYN scan to detect open ports and OS fingerprinting",
        }
        mock_run_in_threadpool.return_value = json.dumps(mock_response)
        mock_request.app.state.chatbot = mock_chatbot.return_value

        result = await generate_command(prompt_request, mock_request)

        assert isinstance(result, CommandGenerationResponse)
        assert result.commands == mock_response["commands"]
        assert result.explanation == mock_response["explanation"]
        mock_chatbot.return_value.prompt_command_generation.assert_called_once_with(task="scan for open ports")

    @pytest.mark.asyncio
    async def test_generate_command_with_json_cleaning(
        self, mock_run_in_threadpool: MagicMock, mock_request: MagicMock, mock_chatbot: MagicMock
    ) -> None:
        """Test command generation with malformed JSON that needs cleaning."""
        prompt_request = PromptRequest(prompt="scan ports")
        malformed_json = '{"commands": ["nmap -sS target", "explanation": "SYN scan"],}'
        mock_run_in_threadpool.return_value = malformed_json
        mock_request.app.state.chatbot = mock_chatbot.return_value

        result = await generate_command(prompt_request, mock_request)

        assert isinstance(result, CommandGenerationResponse)
        assert result.commands == ["nmap -sS target"]
        assert result.explanation == "SYN scan"
        mock_chatbot.return_value.prompt_command_generation.assert_called_once_with(task="scan ports")

    @pytest.mark.asyncio
    async def test_generate_command_missing_keys(
        self, mock_run_in_threadpool: MagicMock, mock_request: MagicMock, mock_chatbot: MagicMock
    ) -> None:
        """Test command generation with missing required keys in LLM response."""
        prompt_request = PromptRequest(prompt="test command")
        mock_response = {"commands": ["ls -la"]}
        mock_run_in_threadpool.return_value = json.dumps(mock_response)
        mock_request.app.state.chatbot = mock_chatbot.return_value

        result = await generate_command(prompt_request, mock_request)

        assert isinstance(result, CommandGenerationResponse)
        assert result.commands == []
        assert "Missing required keys in LLM response" in result.explanation
        assert "explanation" in result.explanation

    @pytest.mark.asyncio
    async def test_generate_command_invalid_json(
        self, mock_run_in_threadpool: MagicMock, mock_request: MagicMock, mock_chatbot: MagicMock
    ) -> None:
        """Test command generation with invalid JSON response from LLM."""
        prompt_request = PromptRequest(prompt="test command")
        mock_run_in_threadpool.return_value = "invalid json response"
        mock_request.app.state.chatbot = mock_chatbot.return_value

        with pytest.raises(HTTPException) as exc_info:
            await generate_command(prompt_request, mock_request)

        assert exc_info.value.status_code == HTTP_INTERNAL_SERVER_ERROR
        detail = exc_info.value.detail
        assert "Invalid JSON response from LLM" in detail["error"]  # type: ignore[index]
        assert "JSON parsing failed" in detail["details"]  # type: ignore[index]
        assert "invalid json response" in detail["raw"]  # type: ignore[index]

    @pytest.mark.asyncio
    async def test_generate_command_llm_exception(
        self, mock_run_in_threadpool: MagicMock, mock_request: MagicMock, mock_chatbot: MagicMock
    ) -> None:
        """Test command generation when LLM raises an exception."""
        prompt_request = PromptRequest(prompt="test command")
        mock_run_in_threadpool.side_effect = Exception("LLM connection failed")
        mock_request.app.state.chatbot = mock_chatbot.return_value

        with pytest.raises(HTTPException) as exc_info:
            await generate_command(prompt_request, mock_request)

        assert exc_info.value.status_code == HTTP_INTERNAL_SERVER_ERROR
        detail = exc_info.value.detail
        assert "Failed to generate or parse LLM response" in detail["error"]  # type: ignore[index]
        assert "LLM connection failed" in detail["details"]  # type: ignore[index]

    @pytest.mark.asyncio
    async def test_generate_command_empty_response(
        self, mock_run_in_threadpool: MagicMock, mock_request: MagicMock, mock_chatbot: MagicMock
    ) -> None:
        """Test command generation with empty response from LLM."""
        prompt_request = PromptRequest(prompt="test command")
        mock_run_in_threadpool.return_value = None
        mock_request.app.state.chatbot = mock_chatbot.return_value

        with pytest.raises(HTTPException) as exc_info:
            await generate_command(prompt_request, mock_request)

        assert exc_info.value.status_code == HTTP_INTERNAL_SERVER_ERROR
        detail = exc_info.value.detail
        assert "No response" in detail["raw"]  # type: ignore[index]


class TestGenerateCommandIntegration:
    """Integration tests for the generate_command endpoint using TestClient."""

    def test_generate_command_endpoint_success(self, mock_run_in_threadpool: MagicMock, test_app: TestClient) -> None:
        """Test the generate_command endpoint through HTTP request."""
        mock_response = {"commands": ["nmap -sT 192.168.1.1"], "explanation": "TCP connect scan of target host"}
        mock_run_in_threadpool.return_value = json.dumps(mock_response)

        response = test_app.post("/api/generate-command", json={"prompt": "scan host 192.168.1.1"})

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["commands"] == mock_response["commands"]
        assert data["explanation"] == mock_response["explanation"]

    def test_generate_command_endpoint_with_malformed_json(
        self, mock_run_in_threadpool: MagicMock, test_app: TestClient
    ) -> None:
        """Test the generate_command endpoint with malformed JSON that gets cleaned."""
        # Simulate malformed JSON response from LLM
        malformed_json = '{"commands": ["nmap -A target", "explanation": "Aggressive scan"],}'
        mock_run_in_threadpool.return_value = malformed_json

        response = test_app.post("/api/generate-command", json={"prompt": "aggressive scan"})

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["commands"] == ["nmap -A target"]
        assert data["explanation"] == "Aggressive scan"

    def test_generate_command_endpoint_invalid_request(self, test_app: TestClient) -> None:
        """Test the generate_command endpoint with invalid request data."""
        response = test_app.post(
            "/api/generate-command",
            json={},
        )

        assert response.status_code == HTTP_UNPROCESSABLE_ENTITY

    def test_generate_command_endpoint_server_error(
        self, mock_run_in_threadpool: MagicMock, test_app: TestClient
    ) -> None:
        """Test the generate_command endpoint when server error occurs."""
        mock_run_in_threadpool.side_effect = Exception("Server error")

        response = test_app.post("/api/generate-command", json={"prompt": "test command"})

        assert response.status_code == HTTP_INTERNAL_SERVER_ERROR
        data = response.json()
        assert "Failed to generate or parse LLM response" in data["detail"]["error"]


class TestRun:
    """Unit tests for the run function."""

    def test_run_function(
        self, mock_create_app: MagicMock, mock_load_config: MagicMock, mock_uvicorn_run: MagicMock, mock_config: Config
    ) -> None:
        """Test the run function orchestrates all components correctly."""
        mock_load_config.return_value = mock_config
        mock_app = MagicMock()
        mock_create_app.return_value = mock_app

        run()

        mock_load_config.assert_called_once()
        mock_create_app.assert_called_once_with(mock_config)
        mock_app.include_router.assert_called_once_with(api_router)
        mock_uvicorn_run.assert_called_once_with(
            mock_app,
            host=mock_config.host,
            port=mock_config.port,
        )
