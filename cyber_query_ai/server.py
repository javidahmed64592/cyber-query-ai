"""Server for the CyberQueryAI application."""

import json
import logging

from fastapi import HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
from python_template_server.models import BaseResponse, ResponseCode
from python_template_server.template_server import TemplateServer

from cyber_query_ai.chatbot import Chatbot
from cyber_query_ai.helpers import (
    clean_json_response,
    get_rag_tools_path,
    get_static_dir,
    get_static_files,
    sanitize_text,
)
from cyber_query_ai.models import (
    CyberQueryAIConfig,
    GetApiConfigResponse,
    PostChatRequest,
    PostChatResponse,
    PostCodeExplanationResponse,
    PostCodeGenerationResponse,
    PostExploitSearchResponse,
    PostLoginResponse,
    PostPromptRequest,
)

logger = logging.getLogger(__name__)

CHAT_FIELDS = PostChatResponse.model_fields.keys() - BaseResponse.model_fields.keys()
CODE_GENERATE_FIELDS = PostCodeGenerationResponse.model_fields.keys() - BaseResponse.model_fields.keys()
CODE_EXPLAIN_FIELDS = PostCodeExplanationResponse.model_fields.keys() - BaseResponse.model_fields.keys()
EXPLOIT_SEARCH_FIELDS = PostExploitSearchResponse.model_fields.keys() - BaseResponse.model_fields.keys()


class CyberQueryAIServer(TemplateServer):
    """AI chatbot server application inheriting from TemplateServer."""

    def __init__(self, config: CyberQueryAIConfig | None = None) -> None:
        """Initialise the CyberQueryAIServer by delegating to the template server.

        :param CyberQueryAIConfig config: CyberQueryAI server configuration
        """
        self.config: CyberQueryAIConfig
        super().__init__(package_name="cyber-query-ai", config=config)
        self.config.save_to_file(self.config_filepath)

        self.chatbot = Chatbot(
            model=self.config.model.model,
            embedding_model=self.config.model.embedding_model,
            tools_json_filepath=get_rag_tools_path(),
        )

        self.static_dir = get_static_dir()
        if self.static_dir.exists():
            self.app.mount("/static", StaticFiles(directory=self.static_dir), name="static")

    def validate_config(self, config_data: dict) -> CyberQueryAIConfig:
        """Validate and parse the configuration data into a CyberQueryAIConfig.

        :param dict config_data: Raw configuration data
        :return CyberQueryAIConfig: Validated CyberQueryAI server configuration
        """
        try:
            return CyberQueryAIConfig.model_validate(config_data)  # type: ignore[no-any-return]
        except ValidationError:
            logger.warning("Invalid configuration data, loading default configuration.")
            return CyberQueryAIConfig.model_validate({})  # type: ignore[no-any-return]

    def setup_routes(self) -> None:
        """Set up API routes."""
        super().setup_routes()
        self.add_authenticated_route("/login", self.post_login, PostLoginResponse, methods=["POST"])
        self.add_unauthenticated_route(
            "/config", self.get_api_config, GetApiConfigResponse, methods=["GET"], limited=False
        )
        self.add_authenticated_route("/model/chat", self.post_chat, PostChatResponse, methods=["POST"])
        self.add_authenticated_route(
            "/code/generate", self.post_generate_code, PostCodeGenerationResponse, methods=["POST"]
        )
        self.add_authenticated_route(
            "/code/explain", self.post_explain_code, PostCodeExplanationResponse, methods=["POST"]
        )
        self.add_authenticated_route(
            "/exploit/search", self.post_exploit_search, PostExploitSearchResponse, methods=["POST"]
        )
        self.add_unauthenticated_route("/{full_path:path}", self.serve_spa, None, methods=["GET"], limited=False)

    async def post_login(self, request: Request) -> PostLoginResponse:
        """Handle user login and return a success response."""
        logger.info("User login successful.")
        return PostLoginResponse(
            code=ResponseCode.OK,
            message="Login successful.",
            timestamp=PostLoginResponse.current_timestamp(),
        )

    async def get_api_config(self, request: Request) -> GetApiConfigResponse:
        """Get the API configuration including model configuration and version."""
        logger.info("Received request for API configuration.")
        return GetApiConfigResponse(
            code=ResponseCode.OK,
            message="Successfully retrieved chatbot configuration.",
            timestamp=GetApiConfigResponse.current_timestamp(),
            model=self.config.model,
            version=self.package_metadata["Version"],
        )

    async def post_chat(self, request: Request) -> PostChatResponse:
        """Chat with the AI assistant using conversation history."""
        logger.info("Received chat request.")
        chat_request = PostChatRequest.model_validate(await request.json())
        message = chat_request.message
        history = chat_request.history

        history_text = ""
        for msg in history:
            history_text += f"{msg.role}: {msg.content}\n"

        formatted_prompt = sanitize_text(self.chatbot.prompt_chat(message, history_text))

        try:
            response = await run_in_threadpool(self.chatbot.llm.invoke, formatted_prompt)
            cleaned_response = clean_json_response(str(response.content))
            parsed = json.loads(cleaned_response)

            if missing_keys := CHAT_FIELDS - parsed.keys():
                error_msg = f"Missing required keys in LLM response: {missing_keys}"
                logger.error(error_msg)
                return PostChatResponse(
                    code=ResponseCode.INTERNAL_SERVER_ERROR,
                    message=error_msg,
                    timestamp=PostChatResponse.current_timestamp(),
                    model_message="",
                )

            return PostChatResponse(
                code=ResponseCode.OK,
                message="Successfully generated chat response.",
                timestamp=PostChatResponse.current_timestamp(),
                model_message=parsed["model_message"],
            )
        except json.JSONDecodeError:
            error_msg = f"Invalid JSON response from LLM: {response.content}"
            logger.exception(error_msg)
            return PostChatResponse(
                code=ResponseCode.INTERNAL_SERVER_ERROR,
                message=error_msg,
                timestamp=PostChatResponse.current_timestamp(),
                model_message="",
            )
        except Exception:
            error_msg = "An unexpected error occurred during chat."
            logger.exception(error_msg)
            return PostChatResponse(
                code=ResponseCode.INTERNAL_SERVER_ERROR,
                message=error_msg,
                timestamp=PostChatResponse.current_timestamp(),
                model_message="",
            )

    async def post_generate_code(self, request: Request) -> PostCodeGenerationResponse:
        """Generate cybersecurity code based on user prompt."""
        logger.info("Received code generation request.")
        prompt_request = PostPromptRequest.model_validate(await request.json())
        formatted_prompt = sanitize_text(self.chatbot.prompt_code_generation(prompt_request.prompt))

        try:
            response = await run_in_threadpool(self.chatbot.llm.invoke, formatted_prompt)
            cleaned_response = clean_json_response(str(response.content))
            parsed = json.loads(cleaned_response)

            if missing_keys := CODE_GENERATE_FIELDS - parsed.keys():
                error_msg = f"Missing required keys in LLM response: {missing_keys}"
                logger.error(error_msg)
                return PostCodeGenerationResponse(
                    code=ResponseCode.INTERNAL_SERVER_ERROR,
                    message=error_msg,
                    timestamp=PostCodeGenerationResponse.current_timestamp(),
                    generated_code="",
                    explanation="",
                    language="",
                )

            return PostCodeGenerationResponse(
                code=ResponseCode.OK,
                message="Successfully generated code.",
                timestamp=PostCodeGenerationResponse.current_timestamp(),
                generated_code=parsed["generated_code"],
                explanation=parsed["explanation"],
                language=parsed["language"],
            )
        except json.JSONDecodeError:
            error_msg = f"Invalid JSON response from LLM: {response.content}"
            logger.exception(error_msg)
            return PostCodeGenerationResponse(
                code=ResponseCode.INTERNAL_SERVER_ERROR,
                message=error_msg,
                timestamp=PostCodeGenerationResponse.current_timestamp(),
                generated_code="",
                explanation="",
                language="",
            )
        except Exception:
            error_msg = "An unexpected error occurred during code generation."
            logger.exception(error_msg)
            return PostCodeGenerationResponse(
                code=ResponseCode.INTERNAL_SERVER_ERROR,
                message=error_msg,
                timestamp=PostCodeGenerationResponse.current_timestamp(),
                generated_code="",
                explanation="",
                language="",
            )

    async def post_explain_code(self, request: Request) -> PostCodeExplanationResponse:
        """Explain code step-by-step."""
        logger.info("Received code explanation request.")
        prompt_request = PostPromptRequest.model_validate(await request.json())
        formatted_prompt = sanitize_text(self.chatbot.prompt_code_explanation(prompt_request.prompt))

        try:
            response = await run_in_threadpool(self.chatbot.llm.invoke, formatted_prompt)
            cleaned_response = clean_json_response(str(response.content))
            parsed = json.loads(cleaned_response)

            if missing_keys := CODE_EXPLAIN_FIELDS - parsed.keys():
                error_msg = f"Missing required keys in LLM response: {missing_keys}"
                logger.error(error_msg)
                return PostCodeExplanationResponse(
                    code=ResponseCode.INTERNAL_SERVER_ERROR,
                    message=error_msg,
                    timestamp=PostCodeExplanationResponse.current_timestamp(),
                    explanation="",
                )

            return PostCodeExplanationResponse(
                code=ResponseCode.OK,
                message="Successfully explained code.",
                timestamp=PostCodeExplanationResponse.current_timestamp(),
                explanation=parsed["explanation"],
            )
        except json.JSONDecodeError:
            error_msg = f"Invalid JSON response from LLM: {response.content}"
            logger.exception(error_msg)
            return PostCodeExplanationResponse(
                code=ResponseCode.INTERNAL_SERVER_ERROR,
                message=error_msg,
                timestamp=PostCodeExplanationResponse.current_timestamp(),
                explanation="",
            )
        except Exception:
            error_msg = "An unexpected error occurred during code explanation."
            logger.exception(error_msg)
            return PostCodeExplanationResponse(
                code=ResponseCode.INTERNAL_SERVER_ERROR,
                message=error_msg,
                timestamp=PostCodeExplanationResponse.current_timestamp(),
                explanation="",
            )

    async def post_exploit_search(self, request: Request) -> PostExploitSearchResponse:
        """Search for known exploits based on target description."""
        logger.info("Received exploit search request.")
        prompt_request = PostPromptRequest.model_validate(await request.json())
        formatted_prompt = sanitize_text(self.chatbot.prompt_exploit_search(prompt_request.prompt))

        try:
            response = await run_in_threadpool(self.chatbot.llm.invoke, formatted_prompt)
            cleaned_response = clean_json_response(str(response.content))
            parsed = json.loads(cleaned_response)

            if missing_keys := EXPLOIT_SEARCH_FIELDS - parsed.keys():
                error_msg = f"Missing required keys in LLM response: {missing_keys}"
                logger.error(error_msg)
                return PostExploitSearchResponse(
                    code=ResponseCode.INTERNAL_SERVER_ERROR,
                    message=error_msg,
                    timestamp=PostExploitSearchResponse.current_timestamp(),
                    exploits=[],
                    explanation="",
                )

            return PostExploitSearchResponse(
                code=ResponseCode.OK,
                message="Successfully searched for exploits.",
                timestamp=PostExploitSearchResponse.current_timestamp(),
                exploits=parsed["exploits"],
                explanation=parsed["explanation"],
            )
        except json.JSONDecodeError:
            error_msg = f"Invalid JSON response from LLM: {response.content}"
            logger.exception(error_msg)
            return PostExploitSearchResponse(
                code=ResponseCode.INTERNAL_SERVER_ERROR,
                message=error_msg,
                timestamp=PostExploitSearchResponse.current_timestamp(),
                exploits=[],
                explanation="",
            )
        except Exception:
            error_msg = "An unexpected error occurred during exploit search."
            logger.exception(error_msg)
            return PostExploitSearchResponse(
                code=ResponseCode.INTERNAL_SERVER_ERROR,
                message=error_msg,
                timestamp=PostExploitSearchResponse.current_timestamp(),
                exploits=[],
                explanation="",
            )

    async def serve_spa(self, request: Request, full_path: str) -> FileResponse:
        """Serve the SPA for all non-API routes."""
        if static_files := get_static_files(full_path, self.static_dir):
            return static_files

        raise HTTPException(status_code=404, detail="File not found")
