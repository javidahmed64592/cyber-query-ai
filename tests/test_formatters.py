"""Unit tests for the cyber_query_ai.formatters module."""

from cyber_query_ai.formatters import ResponseFormatter
from cyber_query_ai.models import (
    CommandGenerationResponse,
    ExplanationResponse,
    Exploit,
    ExploitSearchResponse,
    ScriptGenerationResponse,
)


class TestResponseFormatter:
    """Test cases for the ResponseFormatter class."""

    def test_format_command_generation_single_command(self) -> None:
        """Test formatting command generation with a single command."""
        response = CommandGenerationResponse(
            commands=["nmap -sV -p 80,443 192.168.1.1"],
            explanation="Scan ports 80 and 443 on 192.168.1.1 for service versions",
        )

        result = ResponseFormatter.format_command_generation(response)

        assert "Here are the commands you can use:" in result
        assert "```bash" in result
        assert "nmap -sV -p 80,443 192.168.1.1" in result
        assert "**Explanation**:" in result
        assert "Scan ports 80 and 443" in result

    def test_format_command_generation_multiple_commands(self) -> None:
        """Test formatting command generation with multiple commands."""
        response = CommandGenerationResponse(
            commands=[
                "nmap -sV -p 80,443 192.168.1.1",
                "nikto -h http://192.168.1.1",
                "gobuster dir -u http://192.168.1.1 -w /path/to/wordlist",
            ],
            explanation="Web server reconnaissance commands",
        )

        result = ResponseFormatter.format_command_generation(response)

        assert "```bash" in result
        assert "nmap -sV" in result
        assert "nikto -h" in result
        assert "gobuster dir" in result
        assert all(cmd in result for cmd in response.commands)

    def test_format_command_generation_empty_commands(self) -> None:
        """Test formatting when no commands could be generated."""
        response = CommandGenerationResponse(
            commands=[],
            explanation="Unable to generate commands for this request",
        )

        result = ResponseFormatter.format_command_generation(response)

        assert "I couldn't generate commands" in result
        assert "Unable to generate commands" in result
        assert "```bash" not in result

    def test_format_script_generation_python(self) -> None:
        """Test formatting Python script generation responses."""
        response = ScriptGenerationResponse(
            script="#!/usr/bin/env python3\nimport socket\nprint('Hello World')",
            explanation="A simple Python script that prints Hello World",
        )

        result = ResponseFormatter.format_script_generation(response, "python")

        assert "I've written a python script for you:" in result
        assert "```python" in result
        assert "import socket" in result
        assert "**How it works**:" in result
        assert "simple Python script" in result

    def test_format_script_generation_bash(self) -> None:
        """Test formatting Bash script generation responses."""
        response = ScriptGenerationResponse(
            script="#!/bin/bash\necho 'Test'\nexit 0",
            explanation="A test bash script that echoes Test",
        )

        result = ResponseFormatter.format_script_generation(response, "bash")

        assert "I've written a bash script for you:" in result
        assert "```bash" in result
        assert "echo 'Test'" in result
        assert "**How it works**:" in result

    def test_format_script_generation_powershell(self) -> None:
        """Test formatting PowerShell script generation responses."""
        response = ScriptGenerationResponse(
            script="Write-Host 'Hello from PowerShell'",
            explanation="PowerShell script to display a message",
        )

        result = ResponseFormatter.format_script_generation(response, "powershell")

        assert "```powershell" in result
        assert "Write-Host" in result

    def test_format_explanation_with_context(self) -> None:
        """Test formatting explanation with context."""
        response = ExplanationResponse(
            explanation="This command lists all files in the current directory with detailed information.",
        )

        result = ResponseFormatter.format_explanation(response, "command")

        assert "Let me explain this command:" in result
        assert "lists all files" in result

    def test_format_explanation_script_context(self) -> None:
        """Test formatting explanation with script context."""
        response = ExplanationResponse(
            explanation="This script automates system reconnaissance tasks.",
        )

        result = ResponseFormatter.format_explanation(response, "script")

        assert "Let me explain this script:" in result
        assert "automates system reconnaissance" in result

    def test_format_exploit_search_with_results(self) -> None:
        """Test formatting exploit search with found vulnerabilities."""
        response = ExploitSearchResponse(
            exploits=[
                Exploit(
                    title="CVE-2021-41773",
                    description="Path traversal vulnerability in Apache HTTP Server 2.4.49",
                    severity="CRITICAL",
                    link="https://nvd.nist.gov/vuln/detail/CVE-2021-41773",
                ),
                Exploit(
                    title="CVE-2021-42013",
                    description="Path traversal and RCE in Apache HTTP Server 2.4.49 and 2.4.50",
                    severity="HIGH",
                    link="https://nvd.nist.gov/vuln/detail/CVE-2021-42013",
                ),
            ],
            explanation="Found 2 critical vulnerabilities in Apache 2.4.49",
        )

        result = ResponseFormatter.format_exploit_search(response)

        assert "I found 2 vulnerabilities:" in result
        assert "### CVE-2021-41773 (CRITICAL)" in result
        assert "Path traversal vulnerability" in result
        assert "### CVE-2021-42013 (HIGH)" in result
        assert "**Summary**:" in result
        assert "Found 2 critical vulnerabilities" in result
        assert "https://nvd.nist.gov/vuln/detail/CVE-2021-41773" in result

    def test_format_exploit_search_no_results(self) -> None:
        """Test formatting exploit search with no vulnerabilities found."""
        response = ExploitSearchResponse(
            exploits=[],
            explanation="No known vulnerabilities found for this software version",
        )

        result = ResponseFormatter.format_exploit_search(response)

        assert "No exploits found" in result
        assert "No known vulnerabilities" in result

    def test_format_exploit_search_single_result(self) -> None:
        """Test formatting exploit search with a single vulnerability."""
        response = ExploitSearchResponse(
            exploits=[
                Exploit(
                    title="CVE-2023-12345",
                    description="Test vulnerability",
                    severity="MEDIUM",
                    link="https://example.com/cve-2023-12345",
                ),
            ],
            explanation="One vulnerability found",
        )

        result = ResponseFormatter.format_exploit_search(response)

        assert "I found 1 vulnerability:" in result  # singular form
        assert "### CVE-2023-12345 (MEDIUM)" in result

    def test_format_command_with_multiline_explanation(self) -> None:
        """Test formatting command with multiline explanation."""
        response = CommandGenerationResponse(
            commands=["find . -type f -name '*.log' | xargs grep 'ERROR'"],
            explanation=(
                "This command does several things:\n1. Finds all .log files\n2. Searches for ERROR in each file"
            ),
        )

        result = ResponseFormatter.format_command_generation(response)

        assert "```bash" in result
        assert "find . -type f" in result
        assert "1. Finds all .log files" in result
        assert "2. Searches for ERROR" in result

    def test_format_script_with_special_characters(self) -> None:
        """Test formatting script containing special characters."""
        response = ScriptGenerationResponse(
            script='#!/usr/bin/env python3\nprint("Test < > & \' \\"")',
            explanation="Script with special chars",
        )

        result = ResponseFormatter.format_script_generation(response, "python")

        assert "```python" in result
        # Special characters should be preserved in code blocks
        assert "< > &" in result

    def test_format_exploit_with_markdown_in_description(self) -> None:
        """Test formatting exploit with markdown characters in description."""
        response = ExploitSearchResponse(
            exploits=[
                Exploit(
                    title="CVE-2023-00000",
                    description="Test **vulnerability** with _markdown_",
                    severity="LOW",
                    link="https://example.com",
                ),
            ],
            explanation="Test exploit with markdown",
        )

        result = ResponseFormatter.format_exploit_search(response)

        assert "**vulnerability**" in result
        assert "_markdown_" in result
