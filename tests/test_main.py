"""Unit tests for the cyber_query_ai.main module."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyber_query_ai.api import api_router, limiter
from cyber_query_ai.config import Config
from cyber_query_ai.main import create_app, run

HTTP_OK = 200
HTTP_NOT_FOUND = 404
HTTP_INTERNAL_SERVER_ERROR = 500


@pytest.fixture
def mock_config() -> Config:
    """Fixture for a mock configuration."""
    return Config(model="test-model", embedding_model="test-embedding-model", host="localhost", port=8000)


@pytest.fixture
def mock_chatbot() -> Generator[MagicMock, None, None]:
    """Fixture to create a mock Chatbot class."""
    with patch("cyber_query_ai.main.Chatbot", autospec=True) as mock:
        chatbot_instance = mock.return_value
        chatbot_instance.prompt_command_generation.return_value = "formatted prompt"
        chatbot_instance.llm = MagicMock()
        yield mock


@pytest.fixture
def mock_static_files() -> Generator[MagicMock, None, None]:
    """Fixture to mock StaticFiles in main module."""
    with patch("cyber_query_ai.main.StaticFiles") as mock:
        yield mock


@pytest.fixture
def mock_get_static_dir() -> Generator[MagicMock, None, None]:
    """Fixture to mock get_static_dir function."""
    with patch("cyber_query_ai.main.get_static_dir") as mock:
        yield mock


@pytest.fixture
def mock_get_static_files() -> Generator[MagicMock, None, None]:
    """Fixture to mock get_static_files function."""
    with patch("cyber_query_ai.main.get_static_files") as mock:
        yield mock


@pytest.fixture
def mock_app(
    mock_config: Config,
    mock_chatbot: MagicMock,
    mock_static_files: MagicMock,
    mock_get_static_dir: MagicMock,
    mock_get_static_files: MagicMock,
) -> FastAPI:
    """Fixture to create a test FastAPI app."""
    return create_app(mock_config, api_router, limiter)


@pytest.fixture(autouse=True)
def disable_limiter() -> Generator[None, None, None]:
    """Disable the rate limiter for unit tests."""
    original_enabled = limiter.enabled
    limiter.enabled = False
    yield
    limiter.enabled = original_enabled


class TestCreateApp:
    """Unit tests for the create_app function."""

    def test_create_app_configuration(self, mock_app: FastAPI, mock_config: Config, mock_chatbot: MagicMock) -> None:
        """Test that create_app properly configures the FastAPI application."""
        mock_chatbot.assert_called_once_with(model=mock_config.model, embedding_model=mock_config.embedding_model)
        assert mock_app.state.chatbot == mock_chatbot.return_value
        assert mock_app.state.limiter == limiter

    def test_create_app_cors_settings(self, mock_app: FastAPI, mock_config: Config, mock_chatbot: MagicMock) -> None:
        """Test that CORS middleware is configured with proper settings."""
        cors_middleware = None
        for middleware in mock_app.user_middleware:
            if hasattr(middleware.cls, "__name__") and middleware.cls.__name__ == "CORSMiddleware":
                cors_middleware = middleware
                break

        assert cors_middleware is not None
        assert cors_middleware.kwargs["allow_origins"] == [f"http://{mock_config.host}:{mock_config.port}"]
        assert cors_middleware.kwargs["allow_credentials"] is True
        assert cors_middleware.kwargs["allow_methods"] == ["GET", "POST"]
        assert cors_middleware.kwargs["allow_headers"] == ["Content-Type"]

    def test_create_app_static_files_not_exist(
        self,
        mock_get_static_dir: MagicMock,
        mock_config: Config,
        mock_chatbot: MagicMock,
    ) -> None:
        """Test create_app when static directory doesn't exist."""
        mock_static_dir = MagicMock()
        mock_static_dir.exists.return_value = False
        mock_get_static_dir.return_value = mock_static_dir

        app = create_app(mock_config, api_router, limiter)

        # Should not mount static files or add catch-all route
        static_routes = [
            route for route in app.routes if hasattr(route, "path") and route.path == "/static/{path:path}"
        ]
        assert len(static_routes) == 0

        catch_all_routes = [
            route for route in app.routes if hasattr(route, "path") and route.path == "/{full_path:path}"
        ]
        assert len(catch_all_routes) == 0

    def test_create_app_static_files_exist(
        self,
        mock_static_files: MagicMock,
        mock_get_static_dir: MagicMock,
        mock_config: Config,
        mock_chatbot: MagicMock,
    ) -> None:
        """Test create_app when static directory exists."""
        mock_static_dir = MagicMock()
        mock_static_dir.exists.return_value = True
        mock_get_static_dir.return_value = mock_static_dir

        app = create_app(mock_config, api_router, limiter)

        # Should mount static files
        mock_static_files.assert_called_once_with(directory=mock_static_dir)
        # Should have catch-all route for SPA
        catch_all_routes = [
            route for route in app.routes if hasattr(route, "path") and route.path == "/{full_path:path}"
        ]
        assert len(catch_all_routes) == 1


class TestStaticFileServing:
    """Unit tests for static file serving functionality."""

    def test_spa_route_calls_get_static_files(
        self,
        mock_static_files: MagicMock,
        mock_get_static_dir: MagicMock,
        mock_get_static_files: MagicMock,
        mock_config: Config,
        mock_chatbot: MagicMock,
    ) -> None:
        """Test that SPA route calls get_static_files and handles the response."""
        mock_static_dir = MagicMock()
        mock_static_dir.exists.return_value = True
        mock_get_static_dir.return_value = mock_static_dir

        mock_file_response = MagicMock()
        mock_get_static_files.return_value = mock_file_response

        app = create_app(mock_config, api_router, limiter)
        client = TestClient(app)

        response = client.get("/some-path")

        # Should call get_static_files with the path and static_dir
        mock_get_static_files.assert_called_once_with("some-path", mock_static_dir)
        # Should return the file response
        assert response.status_code == HTTP_OK

    def test_spa_route_handles_file_not_found(
        self,
        mock_static_files: MagicMock,
        mock_get_static_dir: MagicMock,
        mock_get_static_files: MagicMock,
        mock_config: Config,
        mock_chatbot: MagicMock,
    ) -> None:
        """Test that SPA route returns 404 when get_static_files returns None."""
        mock_static_dir = MagicMock()
        mock_static_dir.exists.return_value = True
        mock_get_static_dir.return_value = mock_static_dir

        mock_get_static_files.return_value = None

        app = create_app(mock_config, api_router, limiter)
        client = TestClient(app)

        response = client.get("/non-existent-path")

        assert response.status_code == HTTP_NOT_FOUND
        assert response.json()["detail"] == "File not found"


class TestRun:
    """Unit tests for the run function."""

    @pytest.fixture
    def mock_uvicorn_run(self) -> Generator[MagicMock, None, None]:
        """Fixture to mock uvicorn.run function."""
        with patch("cyber_query_ai.main.uvicorn.run") as mock:
            yield mock

    @pytest.fixture
    def mock_load_config(self) -> Generator[MagicMock, None, None]:
        """Fixture to mock load_config function."""
        with patch("cyber_query_ai.main.load_config") as mock:
            yield mock

    @pytest.fixture
    def mock_create_app(self) -> Generator[MagicMock, None, None]:
        """Fixture to mock create_app function."""
        with patch("cyber_query_ai.main.create_app") as mock:
            yield mock

    def test_run_function(
        self, mock_create_app: MagicMock, mock_load_config: MagicMock, mock_uvicorn_run: MagicMock
    ) -> None:
        """Test the run function orchestrates all components correctly."""
        run()

        mock_load_config.assert_called_once()
        mock_create_app.assert_called_once_with(mock_load_config.return_value, api_router, limiter)
        mock_uvicorn_run.assert_called_once_with(
            mock_create_app.return_value,
            host=mock_load_config.return_value.host,
            port=mock_load_config.return_value.port,
        )
