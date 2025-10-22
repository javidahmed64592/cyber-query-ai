"""Unit tests for the cyber_query_ai.api module."""

import json
from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyber_query_ai.api import api_router, get_server_error, limiter

HTTP_OK = 200
HTTP_UNPROCESSABLE_ENTITY = 422
HTTP_INTERNAL_SERVER_ERROR = 500
DEFAULT_PORT = 8000


@pytest.fixture
def mock_run_in_threadpool() -> Generator[MagicMock, None, None]:
    """Fixture to mock the run_in_threadpool function."""
    with patch("cyber_query_ai.api.run_in_threadpool") as mock:
        yield mock


@pytest.fixture
def mock_clean_json_response() -> Generator[MagicMock, None, None]:
    """Fixture to mock the clean_json_response function."""
    with patch("cyber_query_ai.api.clean_json_response") as mock:
        yield mock


@pytest.fixture(autouse=True)
def disable_limiter() -> Generator[None, None, None]:
    """Disable the rate limiter for unit tests."""
    original_enabled = limiter.enabled
    limiter.enabled = False
    yield
    limiter.enabled = original_enabled


@pytest.fixture
def test_app() -> TestClient:
    """Fixture to create a test FastAPI app."""
    app = FastAPI()
    app.include_router(api_router)
    # Mock the config
    mock_config = MagicMock()
    mock_config.host = "localhost"
    mock_config.port = DEFAULT_PORT
    mock_config.model = "test-model"
    mock_config.embedding_model = "test-embedding-model"
    app.state.config = mock_config
    # Mock the chatbot
    mock_chatbot = MagicMock()
    mock_chatbot.prompt_command_generation.return_value = "formatted prompt"
    mock_chatbot.prompt_script_generation.return_value = "formatted prompt"
    mock_chatbot.prompt_command_explanation.return_value = "formatted prompt"
    mock_chatbot.prompt_script_explanation.return_value = "formatted prompt"
    mock_chatbot.prompt_exploit_search.return_value = "formatted prompt"
    mock_chatbot.llm = MagicMock()
    app.state.chatbot = mock_chatbot
    return TestClient(app)


class TestGetServerError:
    """Tests for the get_server_error function."""

    def test_get_server_error(self) -> None:
        """Test get_server_error returns a 500 response."""
        error = "Something went wrong"
        exception = Exception("Test exception")
        response_text = "Something went wrong"
        server_error = get_server_error(error, exception, response_text)
        assert server_error.status_code == HTTP_INTERNAL_SERVER_ERROR
        assert server_error.detail["error"] == error  # type: ignore[index]
        assert server_error.detail["details"] == str(exception)  # type: ignore[index]
        assert server_error.detail["raw"] == response_text  # type: ignore[index]


class TestHealthCheck:
    """Tests for the health check endpoint."""

    def test_health_check_success(self, test_app: TestClient) -> None:
        """Test successful health check."""
        response = test_app.get("/api/health")

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["timestamp"].endswith("Z")


class TestConfigEndpoint:
    """Tests for the config endpoint."""

    def test_config_endpoint_success(self, test_app: TestClient) -> None:
        """Test successful config retrieval."""
        response = test_app.get("/api/config")

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["host"] == "localhost"
        assert data["port"] == DEFAULT_PORT
        assert data["model"] == "test-model"
        assert data["embedding_model"] == "test-embedding-model"


class TestGenerateCommand:
    """Integration tests for the generate_command endpoint."""

    def test_generate_command_success(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test successful command generation via endpoint."""
        mock_response = {
            "commands": ["nmap -sS -O target"],
            "explanation": "Perform a SYN scan to detect open ports and OS fingerprinting",
        }
        mock_run_in_threadpool.return_value = json.dumps(mock_response)
        mock_clean_json_response.return_value = json.dumps(mock_response)

        response = test_app.post("/api/generate-command", json={"prompt": "scan for open ports"})

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["commands"] == mock_response["commands"]
        assert data["explanation"] == mock_response["explanation"]

    def test_generate_command_with_json_cleaning(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test command generation with malformed JSON that gets cleaned via endpoint."""
        malformed_json = '{"commands": ["nmap -sS target", "explanation": "SYN scan"],}'
        cleaned_json = '{"commands": ["nmap -sS target"], "explanation": "SYN scan"}'
        mock_run_in_threadpool.return_value = malformed_json
        mock_clean_json_response.return_value = cleaned_json

        response = test_app.post("/api/generate-command", json={"prompt": "scan ports"})

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["commands"] == ["nmap -sS target"]
        assert data["explanation"] == "SYN scan"

    def test_generate_command_missing_keys(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test command generation with missing required keys in LLM response via endpoint."""
        mock_response = {"commands": ["ls -la"]}
        mock_run_in_threadpool.return_value = json.dumps(mock_response)
        mock_clean_json_response.return_value = json.dumps(mock_response)

        response = test_app.post("/api/generate-command", json={"prompt": "test command"})

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["commands"] == []
        assert "Missing required keys in LLM response" in data["explanation"]
        assert "explanation" in data["explanation"]

    def test_generate_command_invalid_json(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test command generation with invalid JSON response from LLM via endpoint."""
        mock_run_in_threadpool.return_value = "invalid json response"
        mock_clean_json_response.return_value = "invalid json response"

        response = test_app.post("/api/generate-command", json={"prompt": "test command"})

        assert response.status_code == HTTP_INTERNAL_SERVER_ERROR
        data = response.json()
        assert "Invalid JSON response from LLM" in data["detail"]["error"]
        assert "Expecting value: line 1 column 1 (char 0)" in data["detail"]["details"]
        assert "invalid json response" in data["detail"]["raw"]

    def test_generate_command_llm_exception(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test command generation when LLM raises an exception via endpoint."""
        mock_run_in_threadpool.side_effect = Exception("LLM connection failed")

        response = test_app.post("/api/generate-command", json={"prompt": "test command"})

        assert response.status_code == HTTP_INTERNAL_SERVER_ERROR
        data = response.json()
        assert "Failed to generate or parse LLM response" in data["detail"]["error"]
        assert "LLM connection failed" in data["detail"]["details"]

    def test_generate_command_empty_response(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test command generation with empty response from LLM via endpoint."""
        mock_run_in_threadpool.return_value = None
        mock_clean_json_response.side_effect = lambda x: x

        response = test_app.post("/api/generate-command", json={"prompt": "test command"})

        assert response.status_code == HTTP_INTERNAL_SERVER_ERROR
        data = response.json()
        assert "No response" in data["detail"]["raw"]

    def test_generate_command_endpoint_invalid_request(self, test_app: TestClient) -> None:
        """Test the generate_command endpoint with invalid request data."""
        response = test_app.post(
            "/api/generate-command",
            json={},
        )

        assert response.status_code == HTTP_UNPROCESSABLE_ENTITY


class TestGenerateScript:
    """Integration tests for the generate_script endpoint."""

    def test_generate_script_success(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test successful script generation via endpoint."""
        mock_response = {
            "script": "import socket\ns = socket.socket()\ns.connect(('target', 80))",
            "explanation": "Create a socket connection to test port 80 connectivity",
        }
        mock_run_in_threadpool.return_value = json.dumps(mock_response)
        mock_clean_json_response.return_value = json.dumps(mock_response)

        response = test_app.post("/api/generate-script", json={"prompt": "connect to port 80", "language": "python"})

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["script"] == mock_response["script"]
        assert data["explanation"] == mock_response["explanation"]

    def test_generate_script_missing_keys(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test script generation with missing required keys in LLM response via endpoint."""
        mock_response = {"script": "print('hello')"}
        mock_run_in_threadpool.return_value = json.dumps(mock_response)
        mock_clean_json_response.return_value = json.dumps(mock_response)

        response = test_app.post("/api/generate-script", json={"prompt": "test script", "language": "python"})

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["script"] == ""
        assert "Missing required keys in LLM response" in data["explanation"]
        assert "explanation" in data["explanation"]

    def test_generate_script_invalid_json(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test script generation with invalid JSON response from LLM via endpoint."""
        mock_run_in_threadpool.return_value = "invalid json response"
        mock_clean_json_response.return_value = "invalid json response"

        response = test_app.post("/api/generate-script", json={"prompt": "test script", "language": "python"})

        assert response.status_code == HTTP_INTERNAL_SERVER_ERROR
        data = response.json()
        assert "Invalid JSON response from LLM" in data["detail"]["error"]

    def test_generate_script_endpoint_invalid_request(self, test_app: TestClient) -> None:
        """Test the generate_script endpoint with invalid request data."""
        response = test_app.post(
            "/api/generate-script",
            json={"prompt": "test script"},  # Missing language
        )

        assert response.status_code == HTTP_UNPROCESSABLE_ENTITY


class TestExplainCommand:
    """Integration tests for the explain_command endpoint."""

    def test_explain_command_success(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test successful command explanation via endpoint."""
        mock_response = {
            "explanation": "This nmap command performs a SYN scan on all TCP ports to identify open services",
        }
        mock_run_in_threadpool.return_value = json.dumps(mock_response)
        mock_clean_json_response.return_value = json.dumps(mock_response)

        response = test_app.post("/api/explain-command", json={"prompt": "nmap -sS -p- target"})

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["explanation"] == mock_response["explanation"]

    def test_explain_command_missing_keys(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test command explanation with missing required keys in LLM response via endpoint."""
        mock_response = {"other_key": "value"}
        mock_run_in_threadpool.return_value = json.dumps(mock_response)
        mock_clean_json_response.return_value = json.dumps(mock_response)

        response = test_app.post("/api/explain-command", json={"prompt": "test command"})

        assert response.status_code == HTTP_OK
        data = response.json()
        assert "Missing required keys in LLM response" in data["explanation"]
        assert "explanation" in data["explanation"]

    def test_explain_command_invalid_json(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test command explanation with invalid JSON response from LLM via endpoint."""
        mock_run_in_threadpool.return_value = "invalid json response"
        mock_clean_json_response.return_value = "invalid json response"

        response = test_app.post("/api/explain-command", json={"prompt": "test command"})

        assert response.status_code == HTTP_INTERNAL_SERVER_ERROR
        data = response.json()
        assert "Invalid JSON response from LLM" in data["detail"]["error"]

    def test_explain_command_endpoint_invalid_request(self, test_app: TestClient) -> None:
        """Test the explain_command endpoint with invalid request data."""
        response = test_app.post(
            "/api/explain-command",
            json={},  # Missing prompt
        )

        assert response.status_code == HTTP_UNPROCESSABLE_ENTITY


class TestExplainScript:
    """Integration tests for the explain_script endpoint."""

    def test_explain_script_success(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test successful script explanation via endpoint."""
        mock_response = {
            "explanation": "This Python script creates a socket and attempts to connect to port 80 on the target host",
        }
        mock_run_in_threadpool.return_value = json.dumps(mock_response)
        mock_clean_json_response.return_value = json.dumps(mock_response)

        response = test_app.post("/api/explain-script", json={"prompt": "socket code", "language": "python"})

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["explanation"] == mock_response["explanation"]

    def test_explain_script_missing_keys(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test script explanation with missing required keys in LLM response via endpoint."""
        mock_response = {"other_key": "value"}
        mock_run_in_threadpool.return_value = json.dumps(mock_response)
        mock_clean_json_response.return_value = json.dumps(mock_response)

        response = test_app.post("/api/explain-script", json={"prompt": "test script", "language": "python"})

        assert response.status_code == HTTP_OK
        data = response.json()
        assert "Missing required keys in LLM response" in data["explanation"]
        assert "explanation" in data["explanation"]

    def test_explain_script_invalid_json(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test script explanation with invalid JSON response from LLM via endpoint."""
        mock_run_in_threadpool.return_value = "invalid json response"
        mock_clean_json_response.return_value = "invalid json response"

        response = test_app.post("/api/explain-script", json={"prompt": "test script", "language": "python"})

        assert response.status_code == HTTP_INTERNAL_SERVER_ERROR
        data = response.json()
        assert "Invalid JSON response from LLM" in data["detail"]["error"]

    def test_explain_script_endpoint_invalid_request(self, test_app: TestClient) -> None:
        """Test the explain_script endpoint with invalid request data."""
        response = test_app.post(
            "/api/explain-script",
            json={"prompt": "test script"},  # Missing language
        )

        assert response.status_code == HTTP_UNPROCESSABLE_ENTITY


class TestSearchExploits:
    """Integration tests for the search_exploits endpoint."""

    def test_search_exploits_success(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test successful exploit search via endpoint."""
        mock_response = {
            "exploits": [
                {
                    "title": "CVE-2017-5638",
                    "link": "https://example.com/cve-2017-5638",
                    "severity": "high",
                    "description": "Apache Struts remote code execution vulnerability",
                }
            ],
            "explanation": "Found known vulnerability in Apache Struts 2.3.15.1",
        }
        mock_run_in_threadpool.return_value = json.dumps(mock_response)
        mock_clean_json_response.return_value = json.dumps(mock_response)

        response = test_app.post("/api/search-exploits", json={"prompt": "Apache Struts 2.3.15.1"})

        assert response.status_code == HTTP_OK
        data = response.json()
        assert len(data["exploits"]) == 1
        assert data["exploits"][0]["title"] == "CVE-2017-5638"
        assert data["explanation"] == mock_response["explanation"]

    def test_search_exploits_missing_keys(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test exploit search with missing required keys in LLM response via endpoint."""
        mock_response: dict[str, list] = {"exploits": []}
        mock_run_in_threadpool.return_value = json.dumps(mock_response)
        mock_clean_json_response.return_value = json.dumps(mock_response)

        response = test_app.post("/api/search-exploits", json={"prompt": "test target"})

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["exploits"] == []
        assert "Missing required keys in LLM response" in data["explanation"]
        assert "explanation" in data["explanation"]

    def test_search_exploits_invalid_json(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test exploit search with invalid JSON response from LLM via endpoint."""
        mock_run_in_threadpool.return_value = "invalid json response"
        mock_clean_json_response.return_value = "invalid json response"

        response = test_app.post("/api/search-exploits", json={"prompt": "test target"})

        assert response.status_code == HTTP_INTERNAL_SERVER_ERROR
        data = response.json()
        assert "Invalid JSON response from LLM" in data["detail"]["error"]

    def test_search_exploits_endpoint_invalid_request(self, test_app: TestClient) -> None:
        """Test the search_exploits endpoint with invalid request data."""
        response = test_app.post(
            "/api/search-exploits",
            json={},  # Missing prompt
        )

        assert response.status_code == HTTP_UNPROCESSABLE_ENTITY
