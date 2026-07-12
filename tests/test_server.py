"""Unit tests for the cyber_query_ai.server module."""

from collections.abc import Generator
from importlib.metadata import PackageMetadata
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from cyber_query_ai.chatbot import Chatbot
from cyber_query_ai.models import (
    CyberQueryAIConfig,
)
from cyber_query_ai.routers import ChatbotRouter
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
def mock_server(
    mock_cyber_query_ai_config: CyberQueryAIConfig,
    mock_chatbot_router: ChatbotRouter,
    mock_chatbot: Chatbot,
) -> Generator[CyberQueryAIServer]:
    """Provide a CyberQueryAIServer instance for testing."""
    with (
        patch("cyber_query_ai.server.CyberQueryAIConfig.save_to_file"),
        patch(
            "cyber_query_ai.server.ChatbotRouter",
            return_value=mock_chatbot_router,
            autospec=True,
        ),
        patch("cyber_query_ai.server.Chatbot", return_value=mock_chatbot),
    ):
        server = CyberQueryAIServer(config=mock_cyber_query_ai_config)
        yield server


@pytest.fixture
def mock_client(mock_server: CyberQueryAIServer) -> TestClient:
    """Provide a TestClient for the mock server."""
    return TestClient(mock_server.app)


class TestCyberQueryAIServer:
    """Unit tests for the CyberQueryAIServer class."""

    def test_init(self, mock_server: CyberQueryAIServer) -> None:
        """Test CyberQueryAIServer initialization."""
        assert isinstance(mock_server.config, CyberQueryAIConfig)
        assert isinstance(mock_server._chatbot, Chatbot)

    def test_validate_config(
        self, mock_server: CyberQueryAIServer, mock_cyber_query_ai_config: CyberQueryAIConfig
    ) -> None:
        """Test configuration validation."""
        config_dict = mock_cyber_query_ai_config.model_dump()
        validated_config = mock_server.validate_config(config_dict)
        assert validated_config == mock_cyber_query_ai_config

    def test_validate_config_invalid_returns_default(self, mock_server: CyberQueryAIServer) -> None:
        """Test invalid configuration returns default configuration."""
        invalid_config = {"invalid": None}
        validated_config = mock_server.validate_config(invalid_config)
        assert isinstance(validated_config, CyberQueryAIConfig)
