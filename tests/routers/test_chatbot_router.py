"""Unit tests for the cyber_query_ai.routers.chatbot_router module."""

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException, Request
from fastapi.routing import APIRoute

from cyber_query_ai.models import (
    ChatMessageModel,
    PostChatRequest,
    PostChatResponse,
    PostPromptRequest,
    RoleType,
)
from cyber_query_ai.routers import ChatbotRouter


class TestRoutes:
    """Unit tests for route setup in ChatbotRouter."""

    def test_setup_routes(self, mock_chatbot_router: ChatbotRouter) -> None:
        """Test that routes are set up correctly."""
        api_routes = [route for route in mock_chatbot_router.router.routes if isinstance(route, APIRoute)]
        routes = [route.path for route in api_routes]
        expected_endpoints = [
            "/chatbot/model/chat",
            "/chatbot/code/generate",
            "/chatbot/code/explain",
            "/chatbot/exploit/search",
        ]
        for endpoint in expected_endpoints:
            assert endpoint in routes

    def test_validate_keys(self, mock_chatbot_router: ChatbotRouter) -> None:
        """Test validation of required keys in response dictionary."""
        required_keys = {"key1", "key2", "key3"}
        response_dict = {"key1": "value1", "key2": "value2"}
        with pytest.raises(KeyError):
            mock_chatbot_router.validate_keys(required_keys, response_dict)

    def test_parse_response(
        self, mock_chatbot_router: ChatbotRouter, mock_post_chat_response: PostChatResponse
    ) -> None:
        """Test parsing JSON response strings."""
        response_str = json.dumps(mock_post_chat_response.model_dump())
        parsed = mock_chatbot_router.parse_response(response_str)
        assert parsed == mock_post_chat_response.model_dump()


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
        self, mock_chatbot_router: ChatbotRouter, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test the /model/chat method handles valid JSON and returns a model reply."""
        mock_response = MagicMock()
        mock_response.content = json.dumps({"model_message": "Cybersecurity is the practice of protecting systems..."})
        mock_chatbot.llm.invoke.return_value = mock_response
        response = asyncio.run(mock_chatbot_router.post_chat(mock_request_object))

        assert response.message == "Successfully generated chat response."
        assert isinstance(response.timestamp, str)
        assert response.timestamp.endswith("Z")
        assert isinstance(response.model_message, str)

    def test_post_chat_invalid_json(
        self, mock_chatbot_router: ChatbotRouter, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test /model/chat handles invalid JSON response from LLM."""
        mock_response = MagicMock()
        mock_response.content = "Not valid JSON"
        mock_chatbot.llm.invoke.return_value = mock_response

        with pytest.raises(HTTPException, match="Invalid JSON response from LLM: Not valid JSON"):
            asyncio.run(mock_chatbot_router.post_chat(mock_request_object))

    def test_post_chat_missing_keys(
        self, mock_chatbot_router: ChatbotRouter, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test /model/chat handles missing keys in LLM response."""
        mock_response = MagicMock()
        mock_response.content = json.dumps({"msg": "Missing model_message key"})
        mock_chatbot.llm.invoke.return_value = mock_response

        with pytest.raises(HTTPException, match=r"LLM response missing required keys."):
            asyncio.run(mock_chatbot_router.post_chat(mock_request_object))

    def test_post_chat_error(
        self, mock_chatbot_router: ChatbotRouter, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test /model/chat handles errors gracefully."""
        mock_chatbot.llm.invoke.side_effect = Exception("LLM error")

        with pytest.raises(HTTPException, match=r"An unexpected error occurred during chat."):
            asyncio.run(mock_chatbot_router.post_chat(mock_request_object))


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
        self, mock_chatbot_router: ChatbotRouter, mock_chatbot: MagicMock, mock_request_object: MagicMock
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
        response = asyncio.run(mock_chatbot_router.post_generate_code(mock_request_object))

        assert response.message == "Successfully generated code."
        assert isinstance(response.timestamp, str)
        assert response.timestamp.endswith("Z")
        assert response.generated_code == "ls -la"
        assert response.explanation == "Lists all files in long format"
        assert response.language == "bash"

    def test_post_generate_code_invalid_json(
        self, mock_chatbot_router: ChatbotRouter, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test /code/generate handles invalid JSON response from LLM."""
        mock_response = MagicMock()
        mock_response.content = "Not valid JSON"
        mock_chatbot.llm.invoke.return_value = mock_response

        with pytest.raises(HTTPException, match="Invalid JSON response"):
            asyncio.run(mock_chatbot_router.post_generate_code(mock_request_object))

    def test_post_generate_code_missing_keys(
        self, mock_chatbot_router: ChatbotRouter, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test /code/generate handles missing keys in LLM response."""
        mock_response = MagicMock()
        mock_response.content = json.dumps({"code": "ls"})
        mock_chatbot.llm.invoke.return_value = mock_response

        with pytest.raises(HTTPException, match="LLM response missing required keys"):
            asyncio.run(mock_chatbot_router.post_generate_code(mock_request_object))

    def test_post_generate_code_error(
        self, mock_chatbot_router: ChatbotRouter, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test /code/generate handles errors gracefully."""
        mock_chatbot.llm.invoke.side_effect = Exception("LLM error")

        with pytest.raises(HTTPException, match="An unexpected error occurred during code generation"):
            asyncio.run(mock_chatbot_router.post_generate_code(mock_request_object))


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
        self, mock_chatbot_router: ChatbotRouter, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test the /code/explain method handles valid JSON and returns explanation."""
        mock_response = MagicMock()
        mock_response.content = json.dumps(
            {
                "explanation": "This performs a TCP SYN scan on the target",
            }
        )
        mock_chatbot.llm.invoke.return_value = mock_response
        response = asyncio.run(mock_chatbot_router.post_explain_code(mock_request_object))

        assert response.message == "Successfully explained code."
        assert isinstance(response.timestamp, str)
        assert response.timestamp.endswith("Z")
        assert response.explanation == "This performs a TCP SYN scan on the target"

    def test_post_explain_code_invalid_json(
        self, mock_chatbot_router: ChatbotRouter, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test /code/explain handles invalid JSON response from LLM."""
        mock_response = MagicMock()
        mock_response.content = "Not valid JSON"
        mock_chatbot.llm.invoke.return_value = mock_response

        with pytest.raises(HTTPException, match="Invalid JSON response"):
            asyncio.run(mock_chatbot_router.post_explain_code(mock_request_object))

    def test_post_explain_code_missing_keys(
        self, mock_chatbot_router: ChatbotRouter, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test /code/explain handles missing keys in LLM response."""
        mock_response = MagicMock()
        mock_response.content = json.dumps({})
        mock_chatbot.llm.invoke.return_value = mock_response

        with pytest.raises(HTTPException, match="LLM response missing required keys"):
            asyncio.run(mock_chatbot_router.post_explain_code(mock_request_object))

    def test_post_explain_code_error(
        self, mock_chatbot_router: ChatbotRouter, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test /code/explain handles errors gracefully."""
        mock_chatbot.llm.invoke.side_effect = Exception("LLM error")

        with pytest.raises(HTTPException, match="An unexpected error occurred during code explanation"):
            asyncio.run(mock_chatbot_router.post_explain_code(mock_request_object))


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
        self, mock_chatbot_router: ChatbotRouter, mock_chatbot: MagicMock, mock_request_object: MagicMock
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
        response = asyncio.run(mock_chatbot_router.post_exploit_search(mock_request_object))

        assert response.message == "Successfully searched for exploits."
        assert isinstance(response.timestamp, str)
        assert response.timestamp.endswith("Z")
        assert len(response.exploits) == 1
        assert response.exploits[0].title == "Apache HTTP Server CVE-2021-41773"
        assert response.explanation == "Found 1 exploit for Apache"

    def test_post_exploit_search_invalid_json(
        self, mock_chatbot_router: ChatbotRouter, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test /exploit/search handles invalid JSON response from LLM."""
        mock_response = MagicMock()
        mock_response.content = "Not valid JSON"
        mock_chatbot.llm.invoke.return_value = mock_response

        with pytest.raises(HTTPException, match="Invalid JSON response"):
            asyncio.run(mock_chatbot_router.post_exploit_search(mock_request_object))

    def test_post_exploit_search_missing_keys(
        self, mock_chatbot_router: ChatbotRouter, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test /exploit/search handles missing keys in LLM response."""
        mock_response = MagicMock()
        mock_response.content = json.dumps({"explan": "Missing keys"})
        mock_chatbot.llm.invoke.return_value = mock_response

        with pytest.raises(HTTPException, match="LLM response missing required keys"):
            asyncio.run(mock_chatbot_router.post_exploit_search(mock_request_object))

    def test_post_exploit_search_error(
        self, mock_chatbot_router: ChatbotRouter, mock_chatbot: MagicMock, mock_request_object: MagicMock
    ) -> None:
        """Test /exploit/search handles errors gracefully."""
        mock_chatbot.llm.invoke.side_effect = Exception("LLM error")

        with pytest.raises(HTTPException, match="An unexpected error occurred during exploit search"):
            asyncio.run(mock_chatbot_router.post_exploit_search(mock_request_object))
