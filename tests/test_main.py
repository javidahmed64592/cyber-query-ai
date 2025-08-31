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
    return Config(model="test-model", host="localhost", port=8000)


@pytest.fixture
def mock_chatbot() -> Generator[MagicMock, None, None]:
    """Fixture to create a mock Chatbot class."""
    with patch("cyber_query_ai.main.Chatbot", autospec=True) as mock:
        chatbot_instance = mock.return_value
        chatbot_instance.prompt_command_generation.return_value = "formatted prompt"
        chatbot_instance.llm = MagicMock()
        yield mock


@pytest.fixture
def mock_path() -> Generator[MagicMock, None, None]:
    """Fixture to mock Path in main module."""
    with patch("cyber_query_ai.main.Path") as mock:
        yield mock


@pytest.fixture
def mock_env_get() -> Generator[MagicMock, None, None]:
    """Fixture to mock os.environ.get in main module."""
    with patch("cyber_query_ai.main.os.environ.get") as mock:
        yield mock


@pytest.fixture
def mock_static_files() -> Generator[MagicMock, None, None]:
    """Fixture to mock StaticFiles in main module."""
    with patch("cyber_query_ai.main.StaticFiles") as mock:
        yield mock


@pytest.fixture
def mock_isdir() -> Generator[MagicMock, None, None]:
    """Fixture to mock os.path.isdir in main module."""
    with patch("cyber_query_ai.main.os.path.isdir", return_value=True) as mock:
        yield mock


@pytest.fixture
def mock_app(
    mock_config: Config,
    mock_chatbot: MagicMock,
    mock_static_files: MagicMock,
    mock_env_get: MagicMock,
    mock_path: MagicMock,
    mock_isdir: MagicMock,
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
        mock_chatbot.assert_called_once_with(model=mock_config.model)
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
        mock_app: FastAPI,
        mock_env_get: MagicMock,
        mock_path: MagicMock,
        mock_config: Config,
        mock_chatbot: MagicMock,
    ) -> None:
        """Test create_app when static directory doesn't exist."""
        mock_env_get.return_value = "/test/dir"
        mock_static_dir = MagicMock()
        mock_static_dir.exists.return_value = False
        mock_path.return_value.__truediv__.return_value = mock_static_dir

        # Should not mount static files or add catch-all route
        static_routes = [
            route for route in mock_app.routes if hasattr(route, "path") and route.path == "/static/{path:path}"
        ]
        assert len(static_routes) == 0

    def test_create_app_static_files_exist(
        self,
        mock_static_files: MagicMock,
        mock_env_get: MagicMock,
        mock_path: MagicMock,
        mock_config: Config,
        mock_chatbot: MagicMock,
    ) -> None:
        """Test create_app when static directory exists."""
        mock_env_get.return_value = "/test/dir"
        mock_static_dir = MagicMock()
        mock_static_dir.exists.return_value = True
        mock_path.return_value.__truediv__.return_value = mock_static_dir

        app = create_app(mock_config, api_router, limiter)

        # Should mount static files
        mock_static_files.assert_called_once_with(directory=mock_static_dir)
        # Should have catch-all route for SPA
        catch_all_routes = [
            route for route in app.routes if hasattr(route, "path") and route.path == "/{full_path:path}"
        ]
        assert len(catch_all_routes) == 1

    def test_create_app_uses_environment_variable(
        self,
        mock_env_get: MagicMock,
        mock_path: MagicMock,
        mock_config: Config,
        mock_chatbot: MagicMock,
    ) -> None:
        """Test that create_app uses CYBER_QUERY_AI_ROOT_DIR environment variable."""
        mock_env_get.return_value = "/custom/root/dir"
        mock_static_dir = MagicMock()
        mock_static_dir.exists.return_value = False
        mock_path.return_value.__truediv__.return_value = mock_static_dir

        create_app(mock_config, api_router, limiter)

        mock_env_get.assert_any_call("CYBER_QUERY_AI_ROOT_DIR", ".")
        mock_path.assert_called_once_with("/custom/root/dir")

    def test_create_app_defaults_to_current_directory(
        self,
        mock_env_get: MagicMock,
        mock_path: MagicMock,
        mock_config: Config,
        mock_chatbot: MagicMock,
    ) -> None:
        """Test that create_app defaults to current directory when env var not set."""
        mock_env_get.return_value = None
        mock_static_dir = MagicMock()
        mock_static_dir.exists.return_value = False
        mock_path.return_value.__truediv__.return_value = mock_static_dir

        create_app(mock_config, api_router, limiter)

        mock_env_get.assert_any_call("CYBER_QUERY_AI_ROOT_DIR", ".")
        mock_path.assert_called_once_with(".")


class TestStaticFileServing:
    """Unit tests for static file serving functionality."""

    def test_spa_route_serves_static_files(
        self,
        mock_isdir: MagicMock,
        mock_env_get: MagicMock,
        mock_path: MagicMock,
        mock_config: Config,
        mock_chatbot: MagicMock,
        mock_static_files: MagicMock,
    ) -> None:
        """Test that SPA route serves static files correctly."""
        mock_env_get.return_value = "/test/dir"
        mock_static_dir = MagicMock()
        mock_static_dir.exists.return_value = True
        mock_path.return_value.__truediv__.return_value = mock_static_dir

        app = create_app(mock_config, api_router, limiter)
        client = TestClient(app)

        # Mock file existence and content
        mock_file_path = MagicMock()
        mock_file_path.is_file.return_value = True
        mock_static_dir.__truediv__.return_value = mock_file_path

        with patch("cyber_query_ai.main.FileResponse") as mock_file_response:
            mock_file_response.return_value = MagicMock()
            client.get("/some-file.js")

            # FileResponse should be called with the correct file path
            mock_file_response.assert_called_once_with(mock_file_path)

    def test_spa_route_fallback_to_index(
        self,
        mock_isdir: MagicMock,
        mock_env_get: MagicMock,
        mock_path: MagicMock,
        mock_config: Config,
        mock_chatbot: MagicMock,
        mock_static_files: MagicMock,
    ) -> None:
        """Test that SPA route falls back to index.html for non-existent files."""
        mock_env_get.return_value = "/test/dir"
        mock_static_dir = MagicMock()
        mock_static_dir.exists.return_value = True
        mock_path.return_value.__truediv__.return_value = mock_static_dir

        app = create_app(mock_config, api_router, limiter)
        client = TestClient(app)

        # Mock file doesn't exist but index.html does
        mock_file_path = MagicMock()
        mock_file_path.is_file.return_value = False
        mock_file_path.is_dir.return_value = False
        mock_static_dir.__truediv__.return_value = mock_file_path

        mock_index_path = MagicMock()
        mock_index_path.exists.return_value = True
        mock_static_dir.__truediv__.side_effect = (
            lambda path: mock_index_path if path == "index.html" else mock_file_path
        )

        with patch("cyber_query_ai.main.FileResponse") as mock_file_response:
            mock_file_response.return_value = MagicMock()
            client.get("/non-existent-page")

            # Should serve index.html for SPA routing
            mock_file_response.assert_called_once_with(mock_index_path)

    def test_spa_route_api_requests_return_404(
        self,
        mock_isdir: MagicMock,
        mock_env_get: MagicMock,
        mock_path: MagicMock,
        mock_config: Config,
        mock_chatbot: MagicMock,
        mock_static_files: MagicMock,
    ) -> None:
        """Test that API requests to SPA route return 404."""
        mock_env_get.return_value = "/test/dir"
        mock_static_dir = MagicMock()
        mock_static_dir.exists.return_value = True
        mock_path.return_value.__truediv__.return_value = mock_static_dir

        app = create_app(mock_config, api_router, limiter)
        client = TestClient(app)

        response = client.get("/api/some-endpoint")

        assert response.status_code == HTTP_NOT_FOUND
        assert response.json()["detail"] == "API endpoint not found"

    def test_spa_route_no_index_html_returns_404(
        self,
        mock_isdir: MagicMock,
        mock_env_get: MagicMock,
        mock_path: MagicMock,
        mock_config: Config,
        mock_chatbot: MagicMock,
        mock_static_files: MagicMock,
    ) -> None:
        """Test that SPA route returns 404 when index.html doesn't exist."""
        mock_env_get.return_value = "/test/dir"
        mock_static_dir = MagicMock()
        mock_static_dir.exists.return_value = True
        mock_path.return_value.__truediv__.return_value = mock_static_dir

        app = create_app(mock_config, api_router, limiter)
        client = TestClient(app)

        # Mock file doesn't exist and index.html doesn't exist
        mock_file_path = MagicMock()
        mock_file_path.is_file.return_value = False
        mock_file_path.is_dir.return_value = False
        mock_static_dir.__truediv__.return_value = mock_file_path

        mock_index_path = MagicMock()
        mock_index_path.exists.return_value = False
        mock_static_dir.__truediv__.side_effect = (
            lambda path: mock_index_path if path == "index.html" else mock_file_path
        )

        response = client.get("/non-existent-page")

        assert response.status_code == HTTP_NOT_FOUND
        assert response.json()["detail"] == "File not found"

    def test_spa_route_serves_directory_index(
        self,
        mock_isdir: MagicMock,
        mock_env_get: MagicMock,
        mock_path: MagicMock,
        mock_config: Config,
        mock_chatbot: MagicMock,
        mock_static_files: MagicMock,
    ) -> None:
        """Test that SPA route serves index.html from directories."""
        mock_env_get.return_value = "/test/dir"
        mock_static_dir = MagicMock()
        mock_static_dir.exists.return_value = True
        mock_path.return_value.__truediv__.return_value = mock_static_dir

        app = create_app(mock_config, api_router, limiter)
        client = TestClient(app)

        # Mock directory with index.html
        mock_dir_path = MagicMock()
        mock_dir_path.is_file.return_value = False
        mock_dir_path.is_dir.return_value = True

        mock_index_in_dir = MagicMock()
        mock_index_in_dir.is_file.return_value = True

        # Mock the path resolution for static_dir
        def mock_static_truediv(path: str) -> MagicMock:
            return mock_dir_path

        mock_static_dir.__truediv__.side_effect = mock_static_truediv

        # Mock the path resolution for the directory
        def mock_dir_truediv(path: str) -> MagicMock:
            return mock_index_in_dir

        mock_dir_path.__truediv__.side_effect = mock_dir_truediv

        with patch("cyber_query_ai.main.FileResponse") as mock_file_response:
            mock_file_response.return_value = MagicMock()
            client.get("/command-generation/")

            # Should serve index.html from the directory
            mock_file_response.assert_called_once_with(mock_index_in_dir)


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
