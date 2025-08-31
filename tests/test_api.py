"""Unit tests for the cyber_query_ai.api module."""

import json
from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyber_query_ai.api import api_router, limiter

HTTP_OK = 200
HTTP_UNPROCESSABLE_ENTITY = 422
HTTP_INTERNAL_SERVER_ERROR = 500


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
    # Mock the chatbot
    mock_chatbot = MagicMock()
    mock_chatbot.prompt_command_generation.return_value = "formatted prompt"
    mock_chatbot.llm = MagicMock()
    app.state.chatbot = mock_chatbot
    return TestClient(app)


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
        assert "JSON parsing failed" in data["detail"]["details"]
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
