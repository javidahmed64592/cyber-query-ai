"""Unit tests for the cyber_query_ai.main module."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from cyber_query_ai.main import run
from cyber_query_ai.models import CyberQueryAIConfig


@pytest.fixture
def mock_server_class(mock_cyber_query_ai_config: CyberQueryAIConfig) -> Generator[MagicMock]:
    """Mock CyberQueryAIServer class."""
    with patch("cyber_query_ai.main.CyberQueryAIServer") as mock_server:
        mock_server.load_config.return_value = mock_cyber_query_ai_config
        yield mock_server


class TestRun:
    """Unit tests for the run function."""

    def test_run(self, mock_server_class: MagicMock) -> None:
        """Test successful server run."""
        run()

        mock_server_class.return_value.run.assert_called_once()
