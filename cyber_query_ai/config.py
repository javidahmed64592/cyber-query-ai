"""Configuration utilities for the CyberQueryAI application."""

import json
import os
from pathlib import Path

from pydantic import BaseModel

CONFIG_FILENAME = "config.json"


class Config(BaseModel):
    """Configuration settings for the CyberQueryAI application."""

    model: str
    host: str
    port: int


def get_root_dir() -> Path:
    """Get the root directory for the CyberQueryAI application."""
    return Path(os.environ.get("CYBER_QUERY_AI_ROOT_DIR", "."))


def get_config_path() -> Path:
    """Get the absolute path to the configuration file."""
    return get_root_dir() / CONFIG_FILENAME


def load_config() -> Config:
    """Load the configuration from the config file."""
    config_path = get_config_path()
    if not config_path.exists():
        msg = f"Configuration file not found: {config_path}"
        raise FileNotFoundError(msg)

    with config_path.open() as f:
        return Config(**json.load(f))
