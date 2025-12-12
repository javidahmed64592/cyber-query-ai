"""Unit tests for the cyber_query_ai.models module."""

import pytest

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


# Application Server Configuration Models
class TestCyberQueryAIModelConfig:
    """Unit tests for the CyberQueryAIModelConfig model."""

    def test_model_dump(
        self,
        mock_cyber_query_ai_model_config: CyberQueryAIModelConfig,
        mock_cyber_query_ai_model_config_dict: dict,
    ) -> None:
        """Test the model_dump method."""
        assert mock_cyber_query_ai_model_config.model_dump() == mock_cyber_query_ai_model_config_dict


class TestCyberQueryAIConfig:
    """Unit tests for the CyberQueryAIConfig model."""

    def test_model_dump(
        self,
        mock_cyber_query_ai_config: CyberQueryAIConfig,
        mock_cyber_query_ai_model_config: CyberQueryAIModelConfig,
    ) -> None:
        """Test the model_dump method."""
        assert mock_cyber_query_ai_config.model.model_dump() == mock_cyber_query_ai_model_config.model_dump()


# Request schemas
class TestRoleType:
    """Unit tests for the RoleType enum."""

    @pytest.mark.parametrize(
        ("role_type", "expected_value"),
        [
            (RoleType.USER, "user"),
            (RoleType.ASSISTANT, "assistant"),
        ],
    )
    def test_role_type_enum(self, role_type: RoleType, expected_value: str) -> None:
        """Test the RoleType enum values."""
        assert role_type.value == expected_value


class TestChatMessageModel:
    """Unit tests for the ChatMessageModel model."""

    def test_model_dump(
        self,
        mock_chat_message_model: ChatMessageModel,
        mock_chat_message_model_dict: dict,
    ) -> None:
        """Test the model_dump method."""
        assert mock_chat_message_model.model_dump() == mock_chat_message_model_dict


class TestPostChatRequest:
    """Unit tests for the PostChatRequest model."""

    def test_model_dump(
        self,
        mock_post_chat_request: PostChatRequest,
        mock_post_chat_request_dict: dict,
    ) -> None:
        """Test the model_dump method."""
        assert mock_post_chat_request.model_dump() == mock_post_chat_request_dict


class TestPostPromptRequest:
    """Unit tests for the PostPromptRequest model."""

    def test_model_dump(
        self,
        mock_post_prompt_request: PostPromptRequest,
        mock_post_prompt_request_dict: dict,
    ) -> None:
        """Test the model_dump method."""
        assert mock_post_prompt_request.model_dump() == mock_post_prompt_request_dict


# Response schemas
class TestPostLoginResponse:
    """Unit tests for the PostLoginResponse model."""

    def test_model_dump(
        self,
        mock_post_login_response: PostLoginResponse,
        mock_post_login_response_dict: dict,
    ) -> None:
        """Test the model_dump method."""
        result = mock_post_login_response.model_dump()
        assert result["code"] == mock_post_login_response_dict["code"]
        assert result["message"] == mock_post_login_response_dict["message"]
        assert result["timestamp"] == mock_post_login_response_dict["timestamp"]


class TestGetApiConfigResponse:
    """Unit tests for the GetApiConfigResponse model."""

    def test_model_dump(
        self,
        mock_get_api_config_response: GetApiConfigResponse,
        mock_get_api_config_response_dict: dict,
    ) -> None:
        """Test the model_dump method."""
        result = mock_get_api_config_response.model_dump()
        assert result["model"] == mock_get_api_config_response_dict["model"]
        assert result["version"] == mock_get_api_config_response_dict["version"]


class TestPostChatResponse:
    """Unit tests for the PostChatResponse model."""

    def test_model_dump(
        self,
        mock_post_chat_response: PostChatResponse,
        mock_post_chat_response_dict: dict,
    ) -> None:
        """Test the model_dump method."""
        result = mock_post_chat_response.model_dump()
        assert result["model_message"] == mock_post_chat_response_dict["model_message"]


class TestPostCodeGenerationResponse:
    """Unit tests for the PostCodeGenerationResponse model."""

    def test_model_dump(
        self,
        mock_post_code_generation_response: PostCodeGenerationResponse,
        mock_post_code_generation_response_dict: dict,
    ) -> None:
        """Test the model_dump method."""
        result = mock_post_code_generation_response.model_dump()
        assert result["generated_code"] == mock_post_code_generation_response_dict["generated_code"]
        assert result["explanation"] == mock_post_code_generation_response_dict["explanation"]
        assert result["language"] == mock_post_code_generation_response_dict["language"]


class TestPostCodeExplanationResponse:
    """Unit tests for the PostCodeExplanationResponse model."""

    def test_model_dump(
        self,
        mock_post_code_explanation_response: PostCodeExplanationResponse,
        mock_post_code_explanation_response_dict: dict,
    ) -> None:
        """Test the model_dump method."""
        result = mock_post_code_explanation_response.model_dump()
        assert result["explanation"] == mock_post_code_explanation_response_dict["explanation"]


class TestExploitModel:
    """Unit tests for the ExploitModel model."""

    def test_model_dump(
        self,
        mock_exploit_model: ExploitModel,
        mock_exploit_model_dict: dict,
    ) -> None:
        """Test the model_dump method."""
        assert mock_exploit_model.model_dump() == mock_exploit_model_dict


class TestPostExploitSearchResponse:
    """Unit tests for the PostExploitSearchResponse model."""

    def test_model_dump(
        self,
        mock_post_exploit_search_response: PostExploitSearchResponse,
        mock_post_exploit_search_response_dict: dict,
    ) -> None:
        """Test the model_dump method."""
        result = mock_post_exploit_search_response.model_dump()
        assert result["exploits"] == mock_post_exploit_search_response_dict["exploits"]
        assert result["explanation"] == mock_post_exploit_search_response_dict["explanation"]
