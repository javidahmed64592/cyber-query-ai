"""Unit tests for the cyber_query_ai.config module."""

from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from cyber_query_ai.chatbot import Chatbot


@pytest.fixture(autouse=True)
def mock_ollama_llm() -> Generator[MagicMock, None, None]:
    """Fixture to mock the OllamaLLM."""
    with patch("cyber_query_ai.chatbot.OllamaLLM", autospec=True) as mock:
        yield mock


@pytest.fixture(autouse=True)
def mock_rag_system() -> Generator[MagicMock, None, None]:
    """Fixture to mock the RAGSystem."""
    with patch("cyber_query_ai.chatbot.RAGSystem.create", autospec=True) as mock:
        mock.return_value.generate_rag_content.return_value = "rag content"
        yield mock


@pytest.fixture
def mock_chatbot() -> Chatbot:
    """Fixture to create a Chatbot instance with mocked OllamaLLM."""
    return Chatbot(
        model="test-model", embedding_model="test-embedding-model", tools_json_filepath=Path("test-tools.json")
    )


class TestChatbot:
    """Unit tests for the Chatbot class."""

    def test_initialization(
        self, mock_chatbot: Chatbot, mock_ollama_llm: MagicMock, mock_rag_system: MagicMock
    ) -> None:
        """Test the initialization of the Chatbot."""
        mock_ollama_llm.assert_called_once_with(model=mock_chatbot.model)
        assert mock_chatbot.llm == mock_ollama_llm.return_value
        mock_rag_system.assert_called_once_with(
            model=mock_chatbot.model,
            embedding_model="test-embedding-model",
            tools_json_filepath=Path("test-tools.json"),
        )

    def test_profile_property(self, mock_chatbot: Chatbot) -> None:
        """Test the profile property."""
        profile = mock_chatbot.profile
        assert "cybersecurity assistant" in profile
        assert "Kali Linux" in profile

    def test_pt_chat_property(self, mock_chatbot: Chatbot, mock_rag_system: MagicMock) -> None:
        """Test the pt_chat property."""
        prompt_template = mock_chatbot.pt_chat
        assert prompt_template.input_variables == ["history", "message"]
        assert "You are chatting with a user about cybersecurity tasks" in prompt_template.template
        assert "{history}" in prompt_template.template
        assert "User: {message}" in prompt_template.template
        assert mock_rag_system.return_value.generate_rag_content.return_value in prompt_template.template

    def test_pt_command_generation_property(self, mock_chatbot: Chatbot, mock_rag_system: MagicMock) -> None:
        """Test the pt_command_generation property."""
        prompt_template = mock_chatbot.pt_command_generation
        assert prompt_template.input_variables == ["prompt"]
        assert "RESPONSE SCENARIOS" in prompt_template.template
        assert "Task: `{prompt}`" in prompt_template.template
        assert mock_rag_system.return_value.generate_rag_content.return_value in prompt_template.template

    def test_pt_script_generation_property(self, mock_chatbot: Chatbot, mock_rag_system: MagicMock) -> None:
        """Test the pt_script_generation property."""
        prompt_template = mock_chatbot.pt_script_generation
        assert prompt_template.input_variables == ["language", "prompt"]
        assert "Write a script in {language}" in prompt_template.template
        assert "Task: `{prompt}`" in prompt_template.template
        assert mock_rag_system.return_value.generate_rag_content.return_value in prompt_template.template

    def test_pt_command_explanation_property(self, mock_chatbot: Chatbot, mock_rag_system: MagicMock) -> None:
        """Test the pt_command_explanation property."""
        prompt_template = mock_chatbot.pt_command_explanation
        assert prompt_template.input_variables == ["prompt"]
        assert "Explain the following CLI command" in prompt_template.template
        assert "Command: `{prompt}`" in prompt_template.template
        assert mock_rag_system.return_value.generate_rag_content.return_value in prompt_template.template

    def test_pt_script_explanation_property(self, mock_chatbot: Chatbot, mock_rag_system: MagicMock) -> None:
        """Test the pt_script_explanation property."""
        prompt_template = mock_chatbot.pt_script_explanation
        assert prompt_template.input_variables == ["language", "prompt"]
        assert "Explain the following {language} script" in prompt_template.template
        assert "Script:\n```\n{prompt}\n```\n" in prompt_template.template
        assert mock_rag_system.return_value.generate_rag_content.return_value in prompt_template.template

    def test_pt_exploit_search_property(self, mock_chatbot: Chatbot, mock_rag_system: MagicMock) -> None:
        """Test the pt_exploit_search property."""
        prompt_template = mock_chatbot.pt_exploit_search
        assert prompt_template.input_variables == ["prompt"]
        assert "suggest known exploits" in prompt_template.template
        assert "Target: `{prompt}`" in prompt_template.template
        assert mock_rag_system.return_value.generate_rag_content.return_value in prompt_template.template

    def test_prompt_chat_method(self, mock_chatbot: Chatbot) -> None:
        """Test the prompt_chat method."""
        message = "Hello, how can I help you?"
        history = "User: Hi\nAssistant: Hello!"
        result = mock_chatbot.prompt_chat(message, history)
        assert result == mock_chatbot.pt_chat.format(history=history, message=message)

    def test_prompt_command_generation_method(self, mock_chatbot: Chatbot) -> None:
        """Test the prompt_command_generation method."""
        prompt = "example task"
        result = mock_chatbot.prompt_command_generation(prompt)
        assert result == mock_chatbot.pt_command_generation.format(prompt=prompt)

    def test_prompt_script_generation_method(self, mock_chatbot: Chatbot) -> None:
        """Test the prompt_script_generation method."""
        language = "python"
        prompt = "example task"
        result = mock_chatbot.prompt_script_generation(language, prompt)
        assert result == mock_chatbot.pt_script_generation.format(language=language, prompt=prompt)

    def test_prompt_command_explanation_method(self, mock_chatbot: Chatbot) -> None:
        """Test the prompt_command_explanation method."""
        prompt = "nmap -p- 192.168.1.1"
        result = mock_chatbot.prompt_command_explanation(prompt)
        assert result == mock_chatbot.pt_command_explanation.format(prompt=prompt)

    def test_prompt_script_explanation_method(self, mock_chatbot: Chatbot) -> None:
        """Test the prompt_script_explanation method."""
        language = "python"
        prompt = "import os\nos.system('ls')"
        result = mock_chatbot.prompt_script_explanation(language, prompt)
        assert result == mock_chatbot.pt_script_explanation.format(language=language, prompt=prompt)

    def test_prompt_exploit_search_method(self, mock_chatbot: Chatbot) -> None:
        """Test the prompt_exploit_search method."""
        prompt = "Apache server on port 80"
        result = mock_chatbot.prompt_exploit_search(prompt)
        assert result == mock_chatbot.pt_exploit_search.format(prompt=prompt)
