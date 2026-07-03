"""Chatbot router for CyberQueryAI."""

import json
import logging

from fastapi import HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from python_template_server.models import BaseResponse, ResponseCode
from python_template_server.routers import BaseRouter

from cyber_query_ai.chatbot import Chatbot
from cyber_query_ai.helpers import clean_json_response, sanitize_text
from cyber_query_ai.models import (
    PostChatRequest,
    PostChatResponse,
    PostCodeExplanationResponse,
    PostCodeGenerationResponse,
    PostExploitSearchResponse,
    PostPromptRequest,
)

logger = logging.getLogger(__name__)

CHAT_FIELDS = PostChatResponse.model_fields.keys() - BaseResponse.model_fields.keys()
CODE_GENERATE_FIELDS = PostCodeGenerationResponse.model_fields.keys() - BaseResponse.model_fields.keys()
CODE_EXPLAIN_FIELDS = PostCodeExplanationResponse.model_fields.keys() - BaseResponse.model_fields.keys()
EXPLOIT_SEARCH_FIELDS = PostExploitSearchResponse.model_fields.keys() - BaseResponse.model_fields.keys()


class ChatbotRouter(BaseRouter):
    """Router for the chatbot endpoints."""

    def configure_router(self, chatbot: Chatbot) -> None:
        """Configure the router with necessary dependencies."""
        self._chatbot = chatbot

    def setup_routes(self) -> None:
        """Set up the API routes for the system endpoints."""
        self.add_route(
            endpoint="/model/chat",
            handler_function=self.post_chat,
            response_model=PostChatResponse,
            methods=["POST"],
            limited=True,
            authentication_required=True,
        )
        self.add_route(
            endpoint="/code/generate",
            handler_function=self.post_generate_code,
            response_model=PostCodeGenerationResponse,
            methods=["POST"],
            limited=True,
            authentication_required=True,
        )
        self.add_route(
            endpoint="/code/explain",
            handler_function=self.post_explain_code,
            response_model=PostCodeExplanationResponse,
            methods=["POST"],
            limited=True,
            authentication_required=True,
        )
        self.add_route(
            endpoint="/exploit/search",
            handler_function=self.post_exploit_search,
            response_model=PostExploitSearchResponse,
            methods=["POST"],
            limited=True,
            authentication_required=True,
        )

    @staticmethod
    def validate_keys(required_keys: set[str], response_dict: dict) -> None:
        """Validate that all required keys are present in the response dictionary.

        :param set[str] required_keys: Set of required keys
        :param dict response_dict: Response dictionary to validate
        :raises KeyError: If any required keys are missing
        """
        if missing_keys := list(required_keys - response_dict.keys()):
            msg = f"Missing required keys in LLM response: {missing_keys}"
            raise KeyError(msg)

    @staticmethod
    def parse_response(response_str: str) -> dict:
        """Parse the LLM response string into a dictionary.

        :param str response_str: LLM response string
        :return dict: Parsed response dictionary
        """
        cleaned_response = clean_json_response(response_str)
        return json.loads(cleaned_response)  # type: ignore[no-any-return]

    async def post_chat(self, request: Request) -> PostChatResponse:
        """Chat with the AI assistant using conversation history."""
        chat_request = PostChatRequest.model_validate(await request.json())
        logger.info("Received chat request: %s", chat_request.message)

        history_text = ""
        for msg in chat_request.history:
            history_text += f"{msg.role}: {msg.content}\n"

        formatted_prompt = sanitize_text(self._chatbot.prompt_chat(chat_request.message, history_text))

        try:
            model_response = await run_in_threadpool(self._chatbot.llm.invoke, formatted_prompt)
            parsed = self.parse_response(str(model_response.content))
            self.validate_keys(CHAT_FIELDS, parsed)

            logger.info("Successfully generated chat response.")
            return PostChatResponse(
                message="Successfully generated chat response.",
                model_message=parsed["model_message"],
            )
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON response from LLM: {model_response.content}"
            logger.exception(error_msg)
            raise HTTPException(
                status_code=ResponseCode.INTERNAL_SERVER_ERROR,
                detail=error_msg,
            ) from e
        except KeyError as e:
            error_msg = "LLM response missing required keys."
            logger.exception(error_msg)
            raise HTTPException(
                status_code=ResponseCode.INTERNAL_SERVER_ERROR,
                detail=error_msg,
            ) from e
        except Exception as e:
            error_msg = "An unexpected error occurred during chat."
            logger.exception(error_msg)
            raise HTTPException(
                status_code=ResponseCode.INTERNAL_SERVER_ERROR,
                detail=error_msg,
            ) from e

    async def post_generate_code(self, request: Request) -> PostCodeGenerationResponse:
        """Generate cybersecurity code based on user prompt."""
        prompt_request = PostPromptRequest.model_validate(await request.json())
        logger.info("Received code generation request: %s", prompt_request.prompt)
        formatted_prompt = sanitize_text(self._chatbot.prompt_code_generation(prompt_request.prompt))

        try:
            model_response = await run_in_threadpool(self._chatbot.llm.invoke, formatted_prompt)
            parsed = self.parse_response(str(model_response.content))
            self.validate_keys(CODE_GENERATE_FIELDS, parsed)

            logger.info("Successfully generated code.")
            return PostCodeGenerationResponse(
                message="Successfully generated code.",
                generated_code=parsed["generated_code"],
                explanation=parsed["explanation"],
                language=parsed["language"],
            )
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON response from LLM: {model_response.content}"
            logger.exception(error_msg)
            raise HTTPException(
                status_code=ResponseCode.INTERNAL_SERVER_ERROR,
                detail=error_msg,
            ) from e
        except KeyError as e:
            error_msg = "LLM response missing required keys."
            logger.exception(error_msg)
            raise HTTPException(
                status_code=ResponseCode.INTERNAL_SERVER_ERROR,
                detail=error_msg,
            ) from e
        except Exception as e:
            error_msg = "An unexpected error occurred during code generation."
            logger.exception(error_msg)
            raise HTTPException(
                status_code=ResponseCode.INTERNAL_SERVER_ERROR,
                detail=error_msg,
            ) from e

    async def post_explain_code(self, request: Request) -> PostCodeExplanationResponse:
        """Explain code step-by-step."""
        prompt_request = PostPromptRequest.model_validate(await request.json())
        logger.info("Received code explanation request: %s", prompt_request.prompt)
        formatted_prompt = sanitize_text(self._chatbot.prompt_code_explanation(prompt_request.prompt))

        try:
            model_response = await run_in_threadpool(self._chatbot.llm.invoke, formatted_prompt)
            parsed = self.parse_response(str(model_response.content))
            self.validate_keys(CODE_EXPLAIN_FIELDS, parsed)

            logger.info("Successfully explained code.")
            return PostCodeExplanationResponse(
                message="Successfully explained code.",
                explanation=parsed["explanation"],
            )
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON response from LLM: {model_response.content}"
            logger.exception(error_msg)
            raise HTTPException(
                status_code=ResponseCode.INTERNAL_SERVER_ERROR,
                detail=error_msg,
            ) from e
        except KeyError as e:
            error_msg = "LLM response missing required keys."
            logger.exception(error_msg)
            raise HTTPException(
                status_code=ResponseCode.INTERNAL_SERVER_ERROR,
                detail=error_msg,
            ) from e
        except Exception as e:
            error_msg = "An unexpected error occurred during code explanation."
            logger.exception(error_msg)
            raise HTTPException(
                status_code=ResponseCode.INTERNAL_SERVER_ERROR,
                detail=error_msg,
            ) from e

    async def post_exploit_search(self, request: Request) -> PostExploitSearchResponse:
        """Search for known exploits based on target description."""
        prompt_request = PostPromptRequest.model_validate(await request.json())
        logger.info("Received exploit search request: %s", prompt_request.prompt)
        formatted_prompt = sanitize_text(self._chatbot.prompt_exploit_search(prompt_request.prompt))

        try:
            model_response = await run_in_threadpool(self._chatbot.llm.invoke, formatted_prompt)
            parsed = self.parse_response(str(model_response.content))
            self.validate_keys(EXPLOIT_SEARCH_FIELDS, parsed)

            logger.info("Successfully searched for exploits.")
            return PostExploitSearchResponse(
                message="Successfully searched for exploits.",
                exploits=parsed["exploits"],
                explanation=parsed["explanation"],
            )
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON response from LLM: {model_response.content}"
            logger.exception(error_msg)
            raise HTTPException(
                status_code=ResponseCode.INTERNAL_SERVER_ERROR,
                detail=error_msg,
            ) from e
        except KeyError as e:
            error_msg = "LLM response missing required keys."
            logger.exception(error_msg)
            raise HTTPException(
                status_code=ResponseCode.INTERNAL_SERVER_ERROR,
                detail=error_msg,
            ) from e
        except Exception as e:
            error_msg = "An unexpected error occurred during exploit search."
            logger.exception(error_msg)
            raise HTTPException(
                status_code=ResponseCode.INTERNAL_SERVER_ERROR,
                detail=error_msg,
            ) from e
