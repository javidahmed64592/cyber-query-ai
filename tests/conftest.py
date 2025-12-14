"""Pytest fixtures for the CyberQueryAI unit tests."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from prometheus_client import REGISTRY
from python_template_server.models import ResponseCode

from cyber_query_ai.models import (
    ChatMessageModel,
    CyberQueryAIConfig,
    CyberQueryAIModelConfig,
    ExploitModel,
    GetApiConfigResponse,
    PostChatRequest,
    PostChatResponse,
    PostCodeExplanationResponse,
    PostCodeGenerationResponse,
    PostExploitSearchResponse,
    PostLoginResponse,
    PostPromptRequest,
    RoleType,
)


# General fixtures
@pytest.fixture
def mock_exists() -> Generator[MagicMock]:
    """Mock the Path.exists() method."""
    with patch("pathlib.Path.exists") as mock_exists:
        yield mock_exists


@pytest.fixture
def mock_is_file() -> Generator[MagicMock]:
    """Mock the is_file method of Path."""
    with patch("pathlib.Path.is_file") as mock:
        yield mock


@pytest.fixture
def mock_is_dir() -> Generator[MagicMock]:
    """Mock the is_dir method of Path."""
    with patch("pathlib.Path.is_dir") as mock:
        yield mock


@pytest.fixture(autouse=True)
def clear_prometheus_registry() -> Generator[None]:
    """Clear Prometheus registry before each test to avoid duplicate metric errors."""
    # Clear all collectors from the registry
    collectors = list(REGISTRY._collector_to_names.keys())
    for collector in collectors:
        REGISTRY.unregister(collector)
    yield
    # Clear again after the test
    collectors = list(REGISTRY._collector_to_names.keys())
    for collector in collectors:
        REGISTRY.unregister(collector)


# Application Server Configuration Models
@pytest.fixture
def mock_cyber_query_ai_model_config_dict() -> dict:
    """Fixture for CyberQueryAIModelConfig as a dictionary."""
    return {
        "model": "mistral",
        "embedding_model": "bge-m3",
    }


@pytest.fixture
def mock_cyber_query_ai_model_config(
    mock_cyber_query_ai_model_config_dict: dict,
) -> CyberQueryAIModelConfig:
    """Fixture for CyberQueryAIModelConfig model."""
    return CyberQueryAIModelConfig.model_validate(mock_cyber_query_ai_model_config_dict)


@pytest.fixture
def mock_cyber_query_ai_config(
    mock_cyber_query_ai_model_config: CyberQueryAIModelConfig,
) -> CyberQueryAIConfig:
    """Fixture for CyberQueryAIConfig model."""
    return CyberQueryAIConfig(model=mock_cyber_query_ai_model_config)


# Request schemas
@pytest.fixture
def mock_chat_message_model_dict() -> dict:
    """Fixture for ChatMessageModel as a dictionary."""
    return {
        "role": RoleType.USER,
        "content": "Hello, how can I help you?",
    }


@pytest.fixture
def mock_post_chat_request_dict(
    mock_chat_message_model_dict: dict,
) -> dict:
    """Fixture for PostChatRequest as a dictionary."""
    return {
        "message": "What is cybersecurity?",
        "history": [mock_chat_message_model_dict],
    }


@pytest.fixture
def mock_post_prompt_request_dict() -> dict:
    """Fixture for PostPromptRequest as a dictionary."""
    return {
        "prompt": "Generate a command to list all files",
    }


@pytest.fixture
def mock_chat_message_model(
    mock_chat_message_model_dict: dict,
) -> ChatMessageModel:
    """Fixture for ChatMessageModel model."""
    return ChatMessageModel.model_validate(mock_chat_message_model_dict)


@pytest.fixture
def mock_post_chat_request(
    mock_post_chat_request_dict: dict,
) -> PostChatRequest:
    """Fixture for PostChatRequest model."""
    return PostChatRequest.model_validate(mock_post_chat_request_dict)


@pytest.fixture
def mock_post_prompt_request(
    mock_post_prompt_request_dict: dict,
) -> PostPromptRequest:
    """Fixture for PostPromptRequest model."""
    return PostPromptRequest.model_validate(mock_post_prompt_request_dict)


# Response schemas
@pytest.fixture
def mock_post_login_response_dict() -> dict:
    """Fixture for PostLoginResponse as a dictionary."""
    return {
        "code": ResponseCode.OK,
        "message": "Login successful.",
        "timestamp": PostLoginResponse.current_timestamp(),
    }


@pytest.fixture
def mock_get_api_config_response_dict(
    mock_cyber_query_ai_model_config_dict: dict,
) -> dict:
    """Fixture for GetApiConfigResponse as a dictionary."""
    return {
        "code": ResponseCode.OK,
        "message": "Success",
        "timestamp": GetApiConfigResponse.current_timestamp(),
        "model": mock_cyber_query_ai_model_config_dict,
        "version": "1.0.0",
    }


@pytest.fixture
def mock_post_chat_response_dict() -> dict:
    """Fixture for PostChatResponse as a dictionary."""
    return {
        "code": ResponseCode.OK,
        "message": "Success",
        "timestamp": PostChatResponse.current_timestamp(),
        "model_message": "Cybersecurity is the practice of protecting systems...",
    }


@pytest.fixture
def mock_post_code_generation_response_dict() -> dict:
    """Fixture for PostCodeGenerationResponse as a dictionary."""
    return {
        "code": ResponseCode.OK,
        "message": "Success",
        "timestamp": PostCodeGenerationResponse.current_timestamp(),
        "generated_code": "ls -la",
        "explanation": "This command lists all files in long format.",
        "language": "bash",
    }


@pytest.fixture
def mock_post_code_explanation_response_dict() -> dict:
    """Fixture for PostCodeExplanationResponse as a dictionary."""
    return {
        "code": ResponseCode.OK,
        "message": "Success",
        "timestamp": PostCodeExplanationResponse.current_timestamp(),
        "explanation": "This code scans the network for active hosts.",
    }


@pytest.fixture
def mock_exploit_model_dict() -> dict:
    """Fixture for ExploitModel as a dictionary."""
    return {
        "title": "Sample Exploit",
        "link": "http://example.com/exploit",
        "severity": "High",
        "description": "This is a sample exploit description.",
    }


@pytest.fixture
def mock_post_exploit_search_response_dict(
    mock_exploit_model_dict: dict,
) -> dict:
    """Fixture for PostExploitSearchResponse as a dictionary."""
    return {
        "code": ResponseCode.OK,
        "message": "Success",
        "timestamp": PostExploitSearchResponse.current_timestamp(),
        "exploits": [mock_exploit_model_dict],
        "explanation": "Found 1 exploit related to the query.",
    }


@pytest.fixture
def mock_post_login_response(
    mock_post_login_response_dict: dict,
) -> PostLoginResponse:
    """Fixture for PostLoginResponse model."""
    return PostLoginResponse.model_validate(mock_post_login_response_dict)  # type: ignore[no-any-return]


@pytest.fixture
def mock_get_api_config_response(
    mock_get_api_config_response_dict: dict,
) -> GetApiConfigResponse:
    """Fixture for GetApiConfigResponse model."""
    return GetApiConfigResponse.model_validate(mock_get_api_config_response_dict)  # type: ignore[no-any-return]


@pytest.fixture
def mock_post_chat_response(
    mock_post_chat_response_dict: dict,
) -> PostChatResponse:
    """Fixture for PostChatResponse model."""
    return PostChatResponse.model_validate(mock_post_chat_response_dict)  # type: ignore[no-any-return]


@pytest.fixture
def mock_post_code_generation_response(
    mock_post_code_generation_response_dict: dict,
) -> PostCodeGenerationResponse:
    """Fixture for PostCodeGenerationResponse model."""
    return PostCodeGenerationResponse.model_validate(mock_post_code_generation_response_dict)  # type: ignore[no-any-return]


@pytest.fixture
def mock_post_code_explanation_response(
    mock_post_code_explanation_response_dict: dict,
) -> PostCodeExplanationResponse:
    """Fixture for PostCodeExplanationResponse model."""
    return PostCodeExplanationResponse.model_validate(mock_post_code_explanation_response_dict)  # type: ignore[no-any-return]


@pytest.fixture
def mock_exploit_model(
    mock_exploit_model_dict: dict,
) -> ExploitModel:
    """Fixture for ExploitModel model."""
    return ExploitModel.model_validate(mock_exploit_model_dict)


@pytest.fixture
def mock_post_exploit_search_response(
    mock_post_exploit_search_response_dict: dict,
) -> PostExploitSearchResponse:
    """Fixture for PostExploitSearchResponse model."""
    return PostExploitSearchResponse.model_validate(mock_post_exploit_search_response_dict)  # type: ignore[no-any-return]
