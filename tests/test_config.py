"""Unit tests for the cyber_query_ai.config module."""

import json
from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest

from cyber_query_ai.config import (
    get_config_path,
    get_pyproject_path,
    get_root_dir,
    get_tools_filepath,
    get_version,
    load_config,
)
from cyber_query_ai.models import ConfigResponse

CONFIG_FILENAME = "config.json"
PYPROJECT_FILENAME = "pyproject.toml"
TOOLS_FILENAME = "tools.json"

TEST_MODEL = "model"
TEST_EMBEDDING_MODEL = "embedding-model"
TEST_HOST = "localhost"
TEST_PORT = 1234
TEST_VERSION = "x.y.z"


@pytest.fixture
def mock_config() -> ConfigResponse:
    """Fixture for a mock configuration."""
    return ConfigResponse(
        model=TEST_MODEL,
        embedding_model=TEST_EMBEDDING_MODEL,
        host=TEST_HOST,
        port=TEST_PORT,
        version=TEST_VERSION,
    )


@pytest.fixture
def mock_config_file(mock_config: ConfigResponse) -> MagicMock:
    """Fixture that mocks the config file using mock_open."""
    config_dict = mock_config.model_dump()
    config_dict.pop("version", None)
    config_json = json.dumps(config_dict)
    return mock_open(read_data=config_json)  # type: ignore[no-any-return]


@pytest.fixture
def mock_pyproject_file() -> MagicMock:
    """Fixture that mocks the pyproject.toml file."""
    pyproject_content = f'[project]\nversion = "{TEST_VERSION}"\n'.encode()
    return mock_open(read_data=pyproject_content)  # type: ignore[no-any-return]


class TestConfigUtils:
    """Unit tests for the config utility methods."""

    @pytest.fixture
    def mock_root_dir_env_var(self) -> Generator[None]:
        """Fixture for mocking the CYBER_QUERY_AI_ROOT_DIR environment variable."""
        with patch.dict("os.environ", {"CYBER_QUERY_AI_ROOT_DIR": "/mock/path"}):
            yield

    @pytest.fixture
    def mock_get_config_path(self) -> Generator[MagicMock]:
        """Fixture for mocking the get_config_path function."""
        with patch("cyber_query_ai.config.get_config_path") as mock_get_path:
            yield mock_get_path

    def test_get_root_dir_with_root_dir_env_var(self, mock_root_dir_env_var: Generator[None]) -> None:
        """Test get_root_dir using the mock fixture."""
        assert get_root_dir() == Path("/mock/path")

    def test_get_root_dir_without_root_dir_env_var(self) -> None:
        """Test get_root_dir without the environment variable."""
        assert get_root_dir() == Path(".")

    def test_get_config_path_with_root_dir_env_var(self, mock_root_dir_env_var: Generator[None]) -> None:
        """Test get_config_path using the mock fixture."""
        assert get_config_path() == get_root_dir() / CONFIG_FILENAME

    def test_get_config_path_without_root_dir_env_var(self) -> None:
        """Test get_config_path using the mock fixture."""
        assert get_config_path() == get_root_dir() / CONFIG_FILENAME

    def test_get_pyproject_path_with_root_dir_env_var(self, mock_root_dir_env_var: Generator[None]) -> None:
        """Test get_pyproject_path using the mock fixture."""
        assert get_pyproject_path() == get_root_dir() / PYPROJECT_FILENAME

    def test_get_pyproject_path_without_root_dir_env_var(self) -> None:
        """Test get_pyproject_path without the environment variable."""
        assert get_pyproject_path() == get_root_dir() / PYPROJECT_FILENAME

    def test_get_tools_filepath_with_root_dir_env_var(self, mock_root_dir_env_var: Generator[None]) -> None:
        """Test get_tools_filepath using the mock fixture."""
        assert get_tools_filepath() == get_root_dir() / "rag_data" / TOOLS_FILENAME

    def test_get_tools_filepath_without_root_dir_env_var(self) -> None:
        """Test get_tools_filepath without the environment variable."""
        assert get_tools_filepath() == get_root_dir() / "rag_data" / TOOLS_FILENAME

    def test_get_version_with_mock_file(self, mock_pyproject_file: MagicMock) -> None:
        """Test get_version using the mock pyproject.toml file."""
        with patch("cyber_query_ai.config.get_pyproject_path") as mock_get_pyproject_path:
            mock_get_pyproject_path.return_value.exists.return_value = True
            mock_get_pyproject_path.return_value.open = mock_pyproject_file

            version = get_version()
            assert version == TEST_VERSION

    def test_get_version_without_mock_file(self) -> None:
        """Test get_version when pyproject.toml doesn't exist."""
        with patch("cyber_query_ai.config.get_pyproject_path") as mock_get_pyproject_path:
            mock_get_pyproject_path.return_value.exists.return_value = False

            with pytest.raises(FileNotFoundError, match=r"pyproject\.toml not found:"):
                get_version()

    def test_load_config_with_mock_file(
        self,
        mock_config: ConfigResponse,
        mock_config_file: MagicMock,
        mock_pyproject_file: MagicMock,
        mock_get_config_path: MagicMock,
    ) -> None:
        """Test load_config using the mock file fixture."""
        mock_get_config_path.return_value.exists.return_value = True
        mock_get_config_path.return_value.open = mock_config_file

        with patch("cyber_query_ai.config.get_version") as mock_get_version:
            mock_get_version.return_value = TEST_VERSION

            config = load_config()

            assert config.model == mock_config.model
            assert config.embedding_model == mock_config.embedding_model
            assert config.host == mock_config.host
            assert config.port == mock_config.port
            assert config.version == TEST_VERSION

    def test_load_config_without_mock_file(self, mock_get_config_path: MagicMock) -> None:
        """Test load_config without using the mock file fixture."""
        mock_get_config_path.return_value.exists.return_value = False

        with pytest.raises(FileNotFoundError, match="Configuration file not found:"):
            load_config()
