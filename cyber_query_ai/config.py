"""Configuration utilities for the CyberQueryAI application."""

import json
import os
import tomllib
from pathlib import Path

from cyber_query_ai.models import ConfigResponse

CONFIG_FILENAME = "config.json"
PYPROJECT_FILENAME = "pyproject.toml"
TOOLS_FILENAME = "tools.json"


def get_root_dir() -> Path:
    """Get the root directory for the CyberQueryAI application."""
    return Path(os.environ.get("CYBER_QUERY_AI_ROOT_DIR", "."))


def get_config_path() -> Path:
    """Get the absolute path to the configuration file."""
    return get_root_dir() / CONFIG_FILENAME


def get_pyproject_path() -> Path:
    """Get the absolute path to the pyproject.toml file."""
    return get_root_dir() / PYPROJECT_FILENAME


def get_tools_filepath() -> Path:
    """Get the absolute path to the tools JSON file."""
    return get_root_dir() / "rag_data" / TOOLS_FILENAME


def get_version() -> str:
    """Read the version from pyproject.toml."""
    pyproject_path = get_pyproject_path()
    if not pyproject_path.exists():
        msg = f"pyproject.toml not found: {pyproject_path}"
        raise FileNotFoundError(msg)

    with pyproject_path.open("rb") as f:
        pyproject_data = tomllib.load(f)
        return pyproject_data["project"]["version"]


def load_config() -> ConfigResponse:
    """Load the configuration from the config file."""
    config_path = get_config_path()
    if not config_path.exists():
        msg = f"Configuration file not found: {config_path}"
        raise FileNotFoundError(msg)

    with config_path.open() as f:
        config_data = json.load(f)
        config_data["version"] = get_version()
        return ConfigResponse(**config_data)
