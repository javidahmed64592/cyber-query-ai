"""Unit tests for the cyber_query_ai.helpers module."""

import pytest

from cyber_query_ai.helpers import clean_json_response, sanitize_text


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
