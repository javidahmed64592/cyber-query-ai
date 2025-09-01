"""Unit tests for the cyber_query_ai.helpers module."""

from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.responses import FileResponse

from cyber_query_ai.helpers import (
    clean_json_response,
    get_static_dir,
    get_static_files,
    sanitize_dictionary,
    sanitize_text,
)


class TestStaticFiles:
    """Unit tests for the static file serving functions."""

    @pytest.fixture
    def mock_is_file(self) -> Generator[MagicMock, None, None]:
        """Mock the is_file method of Path."""
        with patch("cyber_query_ai.helpers.Path.is_file") as mock:
            yield mock

    @pytest.fixture
    def mock_is_dir(self) -> Generator[MagicMock, None, None]:
        """Mock the is_dir method of Path."""
        with patch("cyber_query_ai.helpers.Path.is_dir") as mock:
            yield mock

    @pytest.fixture
    def mock_exists(self) -> Generator[MagicMock, None, None]:
        """Mock the exists method of Path."""
        with patch("cyber_query_ai.helpers.Path.exists") as mock:
            yield mock

    def test_get_static_dir(self) -> None:
        """Test that get_static_dir returns the correct path."""
        static_dir = get_static_dir()
        assert static_dir == Path("static")

    def test_get_static_files_api_route(self) -> None:
        """Test that get_static_files returns None for API routes."""
        static_dir = get_static_dir()
        response = get_static_files("api/test", static_dir)
        assert response is None

    def test_get_static_files_specific_file(self, mock_is_file: MagicMock) -> None:
        """Test that get_static_files serves a specific static file."""
        static_dir = get_static_dir()
        mock_is_file.side_effect = [True]
        response = get_static_files("test.txt", static_dir)
        assert isinstance(response, FileResponse)
        assert response.path == static_dir / "test.txt"

    def test_get_static_files_directory_with_index(self, mock_is_file: MagicMock, mock_is_dir: MagicMock) -> None:
        """Test that get_static_files serves index.html for a directory."""
        static_dir = get_static_dir()
        mock_is_file.side_effect = [False, True]
        mock_is_dir.side_effect = [True]
        response = get_static_files("some_dir", static_dir)
        assert isinstance(response, FileResponse)
        assert response.path == static_dir / "some_dir" / "index.html"

    def test_get_static_files_fallback_to_index(
        self,
        mock_is_file: MagicMock,
        mock_is_dir: MagicMock,
        mock_exists: MagicMock,
    ) -> None:
        """Test that get_static_files falls back to static/index.html."""
        static_dir = get_static_dir()
        mock_is_file.side_effect = [False]
        mock_is_dir.side_effect = [False]
        mock_exists.side_effect = [True]
        response = get_static_files("nonexistent", static_dir)
        assert isinstance(response, FileResponse)
        assert response.path == static_dir / "index.html"

    def test_get_static_files_not_found(
        self,
        mock_is_file: MagicMock,
        mock_is_dir: MagicMock,
        mock_exists: MagicMock,
    ) -> None:
        """Test that get_static_files returns None when file not found."""
        static_dir = get_static_dir()
        mock_is_file.side_effect = [False]
        mock_is_dir.side_effect = [False]
        mock_exists.side_effect = [False]
        response = get_static_files("nonexistent", static_dir)
        assert response is None


class TestCleanJsonResponse:
    """Unit tests for the clean_json_response function."""

    @pytest.mark.parametrize(
        ("input_json", "expected", "test_description"),
        [
            # Test trailing commas removal
            (
                '{"commands": ["nmap -sS target",], "explanation": "test",}',
                '{"commands": ["nmap -sS target"], "explanation": "test"}',
                "removes trailing commas from arrays and objects",
            ),
            # Test markdown blocks removal
            (
                '```json\n{"commands": ["ls"], "explanation": "list files"}\n```',
                '{"commands": ["ls"], "explanation": "list files"}',
                "removes markdown code blocks",
            ),
            # Test structural issues fix
            (
                '{"commands": ["nmap -sS target", "explanation": "SYN scan"]}',
                '{"commands": ["nmap -sS target"], "explanation": "SYN scan"}',
                "fixes structural issues with explanation inside commands array",
            ),
            # Test whitespace stripping
            (
                '  \n{"commands": ["ls"], "explanation": "test"}  \n',
                '{"commands": ["ls"], "explanation": "test"}',
                "strips leading and trailing whitespace",
            ),
            # Test combined issues
            (
                '```json\n{"commands": ["nmap", "explanation": "scan",], "extra": "data",}\n```',
                '{"commands": ["nmap"], "explanation": "scan", "extra": "data"}',
                "fixes multiple issues simultaneously",
            ),
            # Test valid JSON unchanged
            (
                '{"commands": ["ls"], "explanation": "test"}',
                '{"commands": ["ls"], "explanation": "test"}',
                "leaves valid JSON unchanged except for whitespace",
            ),
            # Test simple single quotes to double quotes conversion
            (
                "{'script': 'print(hello)', 'explanation': 'prints hello'}",
                '{"script": "print(hello)", "explanation": "prints hello"}',
                "converts simple single quotes to double quotes",
            ),
            # Test mixed single and double quotes
            (
                "{'key1': 'value1', \"key2\": \"value2\"}",
                '{"key1": "value1", "key2": "value2"}',
                "handles mixed single and double quotes",
            ),
            # Test single quotes in arrays
            (
                "{'commands': ['cmd1', 'cmd2'], 'explanation': 'test'}",
                '{"commands": ["cmd1", "cmd2"], "explanation": "test"}',
                "converts single quotes in arrays",
            ),
        ],
    )
    def test_clean_json_response(self, input_json: str, expected: str, test_description: str) -> None:
        """Test that clean_json_response function handles various JSON formatting issues."""
        result = clean_json_response(input_json)
        assert result == expected, f"Failed to {test_description}"


class TestSanitizeText:
    """Unit tests for the sanitize_text function."""

    @pytest.mark.parametrize(
        ("input_text", "expected", "test_description"),
        [
            # Test HTML tag removal
            (
                '<script>alert("xss")</script>Hello',
                "Hello",
                "removes script tags and keeps text",
            ),
            # Test tag with attributes removal
            (
                '<a href="http://example.com">Link</a>',
                "Link",
                "removes anchor tag with attributes and keeps text",
            ),
            # Test whitespace stripping
            (
                "  Hello  ",
                "Hello",
                "strips leading and trailing whitespace",
            ),
            # Test normal text unchanged
            (
                "Hello world",
                "Hello world",
                "leaves normal text unchanged",
            ),
            # Test mixed tags and whitespace
            (
                " <b>Bold</b> text ",
                "Bold text",
                "removes tags and strips whitespace",
            ),
            # Test empty string
            (
                "",
                "",
                "handles empty string",
            ),
            # Test only tags
            (
                "<p></p>",
                "",
                "removes empty tags",
            ),
            # Test nested tags
            (
                "<div><p>Hello</p></div>",
                "Hello",
                "removes nested tags and keeps text",
            ),
            # Test script tag removal
            (
                "<script>code</script>",
                "",
                "removes script tags completely",
            ),
        ],
    )
    def test_sanitize_text(self, input_text: str, expected: str, test_description: str) -> None:
        """Test that sanitize_text function handles various input scenarios."""
        result = sanitize_text(input_text)
        assert result == expected, f"Failed to {test_description}"

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("  value1  ", "value1"),
            (["  value2  ", "  value3  "], ["value2", "value3"]),
            (123, 123),
        ],
    )
    def test_sanitize_dictionary(self, value: str | int | list, expected: str | int | list) -> None:
        """Test that sanitize_dictionary function handles various input scenarios."""
        result = sanitize_dictionary({"key": value})
        assert result == {"key": expected}, "Failed to sanitize dictionary"
