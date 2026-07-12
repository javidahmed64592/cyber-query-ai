"""Server for the CyberQueryAI application."""

import logging
from pathlib import Path

from python_template_server.constants import ROOT_DIR
from python_template_server.routers import BaseRouter
from python_template_server.template_server import TemplateServer

from cyber_query_ai.chatbot import Chatbot
from cyber_query_ai.models import CyberQueryAIConfig
from cyber_query_ai.routers import ChatbotRouter

logger = logging.getLogger(__name__)

CHATBOT_ROUTER = ChatbotRouter(prefix="/chatbot")


class CyberQueryAIServer(TemplateServer):
    """AI chatbot server application inheriting from TemplateServer."""

    def __init__(self, config: CyberQueryAIConfig | None = None) -> None:
        """Initialise the CyberQueryAIServer by delegating to the template server.

        :param CyberQueryAIConfig config: CyberQueryAI server configuration
        """
        self._chatbot = Chatbot()
        self.config: CyberQueryAIConfig
        super().__init__(
            package_name="cyber-query-ai",
            config=config,
        )

        self._chatbot.configure(
            model=self.config.model.model,
            embedding_model=self.config.model.embedding_model,
            tools_json_filepath=self.tools_json_filepath,
        )
        logger.info(
            "Initialized Chatbot with LLMs: %s & %s", self.config.model.model, self.config.model.embedding_model
        )

    @property
    def tools_json_filepath(self) -> Path:
        """Get the RAG tools file path."""
        return Path(ROOT_DIR) / "rag_data" / "tools.json"

    @property
    def routers(self) -> list[BaseRouter]:
        """Define the API routers for the server.

        :return list[BaseRouter]: List of API routers
        """
        CHATBOT_ROUTER.configure_router(chatbot=self._chatbot)
        return [CHATBOT_ROUTER]

    def validate_config(self, config_data: dict) -> CyberQueryAIConfig:
        """Validate and parse the configuration data into a CyberQueryAIConfig.

        :param dict config_data: Raw configuration data
        :return CyberQueryAIConfig: Validated CyberQueryAI server configuration
        """
        return CyberQueryAIConfig.model_validate(config_data)  # type: ignore[no-any-return]
