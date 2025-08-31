"""Unit tests for the cyber_query_ai.helpers module."""

import pytest

from cyber_query_ai.helpers import clean_json_response


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
