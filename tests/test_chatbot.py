"""Unit tests for the cyber_query_ai.config module."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from cyber_query_ai.chatbot import Chatbot


@pytest.fixture(autouse=True)
def mock_ollama_llm() -> Generator[MagicMock, None, None]:
    """Fixture to mock the OllamaLLM."""
    with patch("cyber_query_ai.chatbot.OllamaLLM", autospec=True) as mock:
        yield mock


@pytest.fixture
def mock_chatbot() -> Chatbot:
    """Fixture to create a Chatbot instance with mocked OllamaLLM."""
    return Chatbot(model="test-model")


class TestChatbot:
    """Unit tests for the Chatbot class."""

    def test_initialization(self, mock_chatbot: Chatbot, mock_ollama_llm: MagicMock) -> None:
        """Test the initialization of the Chatbot."""
        mock_ollama_llm.assert_called_once_with(model=mock_chatbot.model)
        assert mock_chatbot.llm == mock_ollama_llm.return_value

    def test_profile_property(self, mock_chatbot: Chatbot) -> None:
        """Test the profile property."""
        profile = mock_chatbot.profile
        assert "cybersecurity assistant" in profile
        assert "Kali Linux" in profile
        assert "Respond ONLY in JSON format" in profile

    def test_pt_command_generation_property(self, mock_chatbot: Chatbot) -> None:
        """Test the pt_command_generation property."""
        prompt_template = mock_chatbot.pt_command_generation
        assert prompt_template.input_variables == ["task"]
        assert mock_chatbot.profile in prompt_template.template
        assert "RESPONSE SCENARIOS" in prompt_template.template
        assert "Task: {task}" in prompt_template.template

    def test_prompt_command_generation_method(self, mock_chatbot: Chatbot) -> None:
        """Test the prompt_command_generation method."""
        task = "example task"
        prompt = mock_chatbot.prompt_command_generation(task)
        assert prompt == mock_chatbot.pt_command_generation.format(task=task)
