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
def mock_run_in_threadpool() -> Generator[MagicMock]:
    """Fixture to mock the run_in_threadpool function."""
    with patch("cyber_query_ai.api.run_in_threadpool") as mock:
        yield mock


@pytest.fixture
def mock_clean_json_response() -> Generator[MagicMock]:
    """Fixture to mock the clean_json_response function."""
    with patch("cyber_query_ai.api.clean_json_response") as mock:
        yield mock


@pytest.fixture(autouse=True)
def disable_limiter() -> Generator[None]:
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
    mock_config.model = "test-model"
    mock_config.embedding_model = "test-embedding-model"
    mock_config.host = "localhost"
    mock_config.port = DEFAULT_PORT
    mock_config.version = "1.0.0"
    app.state.config = mock_config
    # Mock the chatbot
    mock_chatbot = MagicMock()
    mock_chatbot.prompt_chat.return_value = "formatted prompt"
    mock_chatbot.prompt_code_generation.return_value = "formatted prompt"
    mock_chatbot.prompt_code_explanation.return_value = "formatted prompt"
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

    def test_get_health_success(self, test_app: TestClient) -> None:
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
        assert data["model"] == "test-model"
        assert data["embedding_model"] == "test-embedding-model"
        assert data["host"] == "localhost"
        assert data["port"] == DEFAULT_PORT
        assert data["version"] == "1.0.0"


class TestChat:
    """Integration tests for the chat endpoint."""

    def test_chat_success_no_history(self, mock_run_in_threadpool: MagicMock, test_app: TestClient) -> None:
        """Test successful chat with no conversation history."""
        mock_response = "Here's how to scan for open ports using nmap..."
        mock_run_in_threadpool.return_value = mock_response

        response = test_app.post(
            "/api/chat",
            json={"message": "How do I scan for open ports?", "history": []},
        )

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["message"] == mock_response

    def test_chat_success_with_history(self, mock_run_in_threadpool: MagicMock, test_app: TestClient) -> None:
        """Test successful chat with conversation history."""
        mock_response = "nmap -sS is a SYN scan that..."
        mock_run_in_threadpool.return_value = mock_response

        history = [
            {"role": "user", "content": "How do I scan for open ports?"},
            {"role": "assistant", "content": "You can use nmap with the -sS flag"},
        ]

        response = test_app.post(
            "/api/chat",
            json={"message": "What does the -sS flag do?", "history": history},
        )

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["message"] == mock_response

    def test_chat_empty_message(self, mock_run_in_threadpool: MagicMock, test_app: TestClient) -> None:
        """Test chat with empty message."""
        mock_response = "I need more information to help you."
        mock_run_in_threadpool.return_value = mock_response

        response = test_app.post(
            "/api/chat",
            json={"message": "", "history": []},
        )

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["message"] == mock_response

    def test_chat_missing_message(self, test_app: TestClient) -> None:
        """Test chat with missing message field."""
        response = test_app.post(
            "/api/chat",
            json={"history": []},
        )

        assert response.status_code == HTTP_UNPROCESSABLE_ENTITY

    def test_chat_invalid_history(self, test_app: TestClient) -> None:
        """Test chat with invalid history format."""
        response = test_app.post(
            "/api/chat",
            json={"message": "test", "history": "invalid"},
        )

        assert response.status_code == HTTP_UNPROCESSABLE_ENTITY

    def test_chat_llm_exception(self, mock_run_in_threadpool: MagicMock, test_app: TestClient) -> None:
        """Test chat when LLM raises an exception."""
        mock_run_in_threadpool.side_effect = Exception("LLM connection failed")

        response = test_app.post(
            "/api/chat",
            json={"message": "test message", "history": []},
        )

        assert response.status_code == HTTP_INTERNAL_SERVER_ERROR
        data = response.json()
        assert "Failed to generate chat response" in data["detail"]["error"]
        assert "LLM connection failed" in data["detail"]["details"]

    def test_chat_empty_history(self, mock_run_in_threadpool: MagicMock, test_app: TestClient) -> None:
        """Test chat explicitly with empty history list."""
        mock_response = "Test response"
        mock_run_in_threadpool.return_value = mock_response

        response = test_app.post(
            "/api/chat",
            json={"message": "test", "history": []},
        )

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["message"] == mock_response

    def test_chat_long_history(self, mock_run_in_threadpool: MagicMock, test_app: TestClient) -> None:
        """Test chat with long conversation history."""
        mock_response = "Based on our previous discussion..."
        mock_run_in_threadpool.return_value = mock_response

        history = []
        for i in range(10):
            history.append({"role": "user", "content": f"Question {i}"})
            history.append({"role": "assistant", "content": f"Answer {i}"})

        response = test_app.post(
            "/api/chat",
            json={"message": "New question", "history": history},
        )

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["message"] == mock_response

    def test_chat_special_characters(self, mock_run_in_threadpool: MagicMock, test_app: TestClient) -> None:
        """Test chat with special characters in message and response."""
        mock_response = "Response with special chars: <>&\"'"
        mock_run_in_threadpool.return_value = mock_response

        response = test_app.post(
            "/api/chat",
            json={"message": "What about <script>alert('xss')</script>?", "history": []},
        )

        assert response.status_code == HTTP_OK
        data = response.json()
        assert "&lt;" in data["message"] or "&gt;" in data["message"] or "&amp;" in data["message"]

    def test_chat_multiline_message(self, mock_run_in_threadpool: MagicMock, test_app: TestClient) -> None:
        """Test chat with multiline message."""
        mock_response = "Here's the explanation..."
        mock_run_in_threadpool.return_value = mock_response

        multiline_message = """How do I use nmap?
        I want to scan for open ports
        on my local network"""

        response = test_app.post(
            "/api/chat",
            json={"message": multiline_message, "history": []},
        )

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["message"] == mock_response


class TestGenerateCode:
    """Integration tests for the generate_code endpoint."""

    def test_generate_code_success(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test successful code generation via endpoint."""
        mock_response = {
            "code": "nmap -sS -O target",
            "explanation": "Perform a SYN scan to detect open ports and OS fingerprinting",
            "language": "bash",
        }
        mock_run_in_threadpool.return_value = json.dumps(mock_response)
        mock_clean_json_response.return_value = json.dumps(mock_response)

        response = test_app.post("/api/generate-code", json={"prompt": "scan for open ports"})

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["code"] == mock_response["code"]
        assert data["explanation"] == mock_response["explanation"]
        assert data["language"] == mock_response["language"]

    def test_generate_code_with_json_cleaning(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test code generation with malformed JSON that gets cleaned via endpoint."""
        malformed_json = '{"code": "nmap -sS target", "explanation": "SYN scan", "language": "bash",}'
        cleaned_json = '{"code": "nmap -sS target", "explanation": "SYN scan", "language": "bash"}'
        mock_run_in_threadpool.return_value = malformed_json
        mock_clean_json_response.return_value = cleaned_json

        response = test_app.post("/api/generate-code", json={"prompt": "scan ports"})

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["code"] == "nmap -sS target"
        assert data["explanation"] == "SYN scan"
        assert data["language"] == "bash"

    def test_generate_code_missing_keys(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test code generation with missing required keys in LLM response via endpoint."""
        mock_response = {"code": "ls -la"}
        mock_run_in_threadpool.return_value = json.dumps(mock_response)
        mock_clean_json_response.return_value = json.dumps(mock_response)

        response = test_app.post("/api/generate-code", json={"prompt": "test command"})

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["code"] == ""
        assert "Missing required keys in LLM response" in data["explanation"]

    def test_generate_code_invalid_json(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test code generation with invalid JSON response via endpoint."""
        mock_run_in_threadpool.return_value = "not valid json at all"
        mock_clean_json_response.return_value = "not valid json at all"

        response = test_app.post("/api/generate-code", json={"prompt": "test"})

        assert response.status_code == HTTP_INTERNAL_SERVER_ERROR
        data = response.json()
        assert "Invalid JSON response from LLM" in data["detail"]["error"]

    def test_generate_code_llm_exception(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test code generation with LLM exception via endpoint."""
        mock_run_in_threadpool.side_effect = Exception("LLM service unavailable")

        response = test_app.post("/api/generate-code", json={"prompt": "test"})

        assert response.status_code == HTTP_INTERNAL_SERVER_ERROR
        data = response.json()
        assert "Failed to generate or parse LLM response" in data["detail"]["error"]
        assert "LLM service unavailable" in data["detail"]["details"]

    def test_generate_code_empty_response(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test code generation with empty code response via endpoint."""
        mock_response = {
            "code": "",
            "explanation": "No suitable tool available for this task",
            "language": "bash",
        }
        mock_run_in_threadpool.return_value = json.dumps(mock_response)
        mock_clean_json_response.return_value = json.dumps(mock_response)

        response = test_app.post("/api/generate-code", json={"prompt": "impossible task"})

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["code"] == ""
        assert "No suitable tool available" in data["explanation"]

    def test_generate_code_endpoint_invalid_request(self, test_app: TestClient) -> None:
        """Test code generation endpoint with invalid request body."""
        response = test_app.post("/api/generate-code", json={})  # Missing prompt

        assert response.status_code == HTTP_UNPROCESSABLE_ENTITY


class TestExplainCode:
    """Integration tests for the explain_code endpoint."""

    def test_explain_code_success(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test successful code explanation via endpoint."""
        mock_response = {
            "explanation": "The nmap command performs network discovery and security auditing",
        }
        mock_run_in_threadpool.return_value = json.dumps(mock_response)
        mock_clean_json_response.return_value = json.dumps(mock_response)

        response = test_app.post("/api/explain-code", json={"prompt": "nmap -sS target"})

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["explanation"] == mock_response["explanation"]

    def test_explain_code_with_json_cleaning(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test code explanation with malformed JSON that gets cleaned via endpoint."""
        malformed_json = '{"explanation": "This command performs a SYN scan",}'
        cleaned_json = '{"explanation": "This command performs a SYN scan"}'
        mock_run_in_threadpool.return_value = malformed_json
        mock_clean_json_response.return_value = cleaned_json

        response = test_app.post("/api/explain-code", json={"prompt": "nmap -sS target"})

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["explanation"] == "This command performs a SYN scan"

    def test_explain_code_missing_keys(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test code explanation with missing required keys in LLM response via endpoint."""
        mock_response: dict[str, str] = {}
        mock_run_in_threadpool.return_value = json.dumps(mock_response)
        mock_clean_json_response.return_value = json.dumps(mock_response)

        response = test_app.post("/api/explain-code", json={"prompt": "test code"})

        assert response.status_code == HTTP_OK
        data = response.json()
        assert "Missing required keys in LLM response" in data["explanation"]

    def test_explain_code_invalid_json(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test code explanation with invalid JSON response via endpoint."""
        mock_run_in_threadpool.return_value = "invalid json"
        mock_clean_json_response.return_value = "invalid json"

        response = test_app.post("/api/explain-code", json={"prompt": "test code"})

        assert response.status_code == HTTP_INTERNAL_SERVER_ERROR
        data = response.json()
        assert "Invalid JSON response from LLM" in data["detail"]["error"]

    def test_explain_code_llm_exception(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test code explanation with LLM exception via endpoint."""
        mock_run_in_threadpool.side_effect = Exception("LLM service unavailable")

        response = test_app.post("/api/explain-code", json={"prompt": "test"})

        assert response.status_code == HTTP_INTERNAL_SERVER_ERROR
        data = response.json()
        assert "Failed to generate or parse LLM response" in data["detail"]["error"]
        assert "LLM service unavailable" in data["detail"]["details"]

    def test_explain_code_empty_response(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test code explanation with empty explanation response via endpoint."""
        mock_response = {
            "explanation": "",
        }
        mock_run_in_threadpool.return_value = json.dumps(mock_response)
        mock_clean_json_response.return_value = json.dumps(mock_response)

        response = test_app.post("/api/explain-code", json={"prompt": "unknown command"})

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["explanation"] == ""

    def test_explain_code_endpoint_invalid_request(self, test_app: TestClient) -> None:
        """Test code explanation endpoint with invalid request body."""
        response = test_app.post("/api/explain-code", json={})  # Missing prompt

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

    def test_search_exploits_with_json_cleaning(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test exploit search with malformed JSON that gets cleaned via endpoint."""
        malformed_json = (
            '{"exploits": [{"title": "CVE-2021-1234", "link": "https://example.com", '
            '"severity": "medium", "description": "Test vuln"}], "explanation": "Found vulnerability",}'
        )
        cleaned_json = (
            '{"exploits": [{"title": "CVE-2021-1234", "link": "https://example.com", '
            '"severity": "medium", "description": "Test vuln"}], "explanation": "Found vulnerability"}'
        )
        mock_run_in_threadpool.return_value = malformed_json
        mock_clean_json_response.return_value = cleaned_json

        response = test_app.post("/api/search-exploits", json={"prompt": "test software"})

        assert response.status_code == HTTP_OK
        data = response.json()
        assert len(data["exploits"]) == 1
        assert data["exploits"][0]["title"] == "CVE-2021-1234"
        assert data["explanation"] == "Found vulnerability"

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

    def test_search_exploits_llm_exception(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test exploit search with LLM exception via endpoint."""
        mock_run_in_threadpool.side_effect = Exception("LLM service unavailable")

        response = test_app.post("/api/search-exploits", json={"prompt": "test"})

        assert response.status_code == HTTP_INTERNAL_SERVER_ERROR
        data = response.json()
        assert "Failed to generate or parse LLM response" in data["detail"]["error"]
        assert "LLM service unavailable" in data["detail"]["details"]

    def test_search_exploits_empty_response(
        self, mock_run_in_threadpool: MagicMock, mock_clean_json_response: MagicMock, test_app: TestClient
    ) -> None:
        """Test exploit search with empty exploits list via endpoint."""
        mock_response = {
            "exploits": [],
            "explanation": "No exploits found for this software version",
        }
        mock_run_in_threadpool.return_value = json.dumps(mock_response)
        mock_clean_json_response.return_value = json.dumps(mock_response)

        response = test_app.post("/api/search-exploits", json={"prompt": "secure software v1.0"})

        assert response.status_code == HTTP_OK
        data = response.json()
        assert data["exploits"] == []
        assert "No exploits found" in data["explanation"]

    def test_search_exploits_endpoint_invalid_request(self, test_app: TestClient) -> None:
        """Test the search_exploits endpoint with invalid request data."""
        response = test_app.post(
            "/api/search-exploits",
            json={},  # Missing prompt
        )

        assert response.status_code == HTTP_UNPROCESSABLE_ENTITY
