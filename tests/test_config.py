"""Unit tests for the cyber_query_ai.config module."""

import json
from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest

from cyber_query_ai.config import Config, get_config_path, get_root_dir, load_config

TEST_MODEL = "model"
TEST_HOST = "localhost"
TEST_PORT = 1234


@pytest.fixture
def mock_config() -> Config:
    """Fixture for a mock configuration."""
    return Config(model=TEST_MODEL, host=TEST_HOST, port=TEST_PORT)


@pytest.fixture
def mock_config_file(mock_config: Config) -> MagicMock:
    """Fixture that mocks the config file using mock_open."""
    config_json = json.dumps(mock_config.model_dump())
    return mock_open(read_data=config_json)  # type: ignore[no-any-return]


class TestConfig:
    """Unit tests for the Config class."""

    def test_model_dump(self, mock_config: Config) -> None:
        """Test the model_dump method."""
        expected = {
            "model": mock_config.model,
            "host": mock_config.host,
            "port": mock_config.port,
        }
        assert mock_config.model_dump() == expected


class TestConfigUtils:
    """Unit tests for the config utility methods."""

    @pytest.fixture
    def mock_root_dir_env_var(self) -> Generator[None, None, None]:
        """Fixture for mocking the CYBER_QUERY_AI_ROOT_DIR environment variable."""
        with patch.dict("os.environ", {"CYBER_QUERY_AI_ROOT_DIR": "/mock/path"}):
            yield

    @pytest.fixture
    def mock_get_config_path(self) -> Generator[MagicMock, None, None]:
        """Fixture for mocking the get_config_path function."""
        with patch("cyber_query_ai.config.get_config_path") as mock_get_path:
            yield mock_get_path

    def test_get_root_dir_with_root_dir_env_var(self, mock_root_dir_env_var: Generator[None, None, None]) -> None:
        """Test get_root_dir using the mock fixture."""
        assert get_root_dir() == Path("/mock/path")

    def test_get_root_dir_without_root_dir_env_var(self) -> None:
        """Test get_root_dir without the environment variable."""
        assert get_root_dir() == Path(".")

    def test_get_config_path_with_root_dir_env_var(self, mock_root_dir_env_var: Generator[None, None, None]) -> None:
        """Test get_config_path using the mock fixture."""
        assert get_config_path() == get_root_dir() / "config.json"

    def test_get_config_path_without_root_dir_env_var(self) -> None:
        """Test get_config_path using the mock fixture."""
        assert get_config_path() == get_root_dir() / "config.json"

    def test_load_config_with_mock_file(
        self, mock_config: Config, mock_config_file: MagicMock, mock_get_config_path: MagicMock
    ) -> None:
        """Test load_config using the mock file fixture."""
        mock_get_config_path.return_value.exists.return_value = True
        mock_get_config_path.return_value.open = mock_config_file

        config = load_config()

        assert config.model == mock_config.model
        assert config.host == mock_config.host
        assert config.port == mock_config.port

    def test_load_config_without_mock_file(self, mock_get_config_path: MagicMock) -> None:
        """Test load_config without using the mock file fixture."""
        mock_get_config_path.return_value.exists.return_value = False

        with pytest.raises(FileNotFoundError, match="Configuration file not found:"):
            load_config()
