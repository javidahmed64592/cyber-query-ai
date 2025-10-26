"""Unit tests for the cyber_query_ai.formatters module."""

from cyber_query_ai.formatters import ResponseFormatter
from cyber_query_ai.models import (
    CodeExplanationResponse,
    CodeGenerationResponse,
    Exploit,
    ExploitSearchResponse,
)


class TestResponseFormatter:
    """Test cases for the ResponseFormatter class."""

    def test_format_code_generation_single_line(self) -> None:
        """Test formatting code generation with a single-line command."""
        response = CodeGenerationResponse(
            code="nmap -sV -p 80,443 192.168.1.1",
            explanation="Scan ports 80 and 443 on 192.168.1.1 for service versions",
            language="bash",
        )

        result = ResponseFormatter.format_code_generation(response)

        assert "Here's the command you can use:" in result
        assert "```bash" in result
        assert "nmap -sV -p 80,443 192.168.1.1" in result
        assert "**Explanation**:" in result
        assert "Scan ports 80 and 443" in result

    def test_format_code_generation_multi_line_bash(self) -> None:
        """Test formatting code generation with multi-line bash script."""
        response = CodeGenerationResponse(
            code="#!/bin/bash\nfor ip in $(seq 1 254); do\n  ping -c 1 192.168.1.$ip\ndone",
            explanation="Script that pings all hosts in the network",
            language="bash",
        )

        result = ResponseFormatter.format_code_generation(response)

        assert "I've written a bash script for you:" in result
        assert "```bash" in result
        assert "for ip in" in result
        assert "ping -c 1" in result
        assert "**Explanation**:" in result

    def test_format_code_generation_python_script(self) -> None:
        """Test formatting Python script generation responses."""
        response = CodeGenerationResponse(
            code="#!/usr/bin/env python3\nimport socket\nprint('Hello World')",
            explanation="A simple Python script that prints Hello World",
            language="python",
        )

        result = ResponseFormatter.format_code_generation(response)

        assert "I've written a python script for you:" in result
        assert "```python" in result
        assert "import socket" in result
        assert "**Explanation**:" in result
        assert "simple Python script" in result

    def test_format_code_generation_empty_code(self) -> None:
        """Test formatting when no code could be generated."""
        response = CodeGenerationResponse(
            code="",
            explanation="Unable to generate code for this request",
            language="bash",
        )

        result = ResponseFormatter.format_code_generation(response)

        assert "I couldn't generate code" in result
        assert "Unable to generate code" in result
        assert "```bash" not in result

    def test_format_code_generation_powershell(self) -> None:
        """Test formatting PowerShell code generation responses."""
        response = CodeGenerationResponse(
            code="Get-Process | Where-Object {$_.CPU -gt 100}",
            explanation="Get processes using more than 100 CPU time",
            language="powershell",
        )

        result = ResponseFormatter.format_code_generation(response)

        assert "```powershell" in result
        assert "Get-Process" in result
        assert "Here's the command you can use:" in result

    def test_format_explanation_default_context(self) -> None:
        """Test formatting explanation with default context."""
        response = CodeExplanationResponse(
            explanation="This command lists all files in the current directory with detailed information.",
        )

        result = ResponseFormatter.format_explanation(response)

        assert "Let me explain this code:" in result
        assert "lists all files" in result

    def test_format_explanation_custom_context(self) -> None:
        """Test formatting explanation with custom context."""
        response = CodeExplanationResponse(
            explanation="This script automates system reconnaissance tasks.",
        )

        result = ResponseFormatter.format_explanation(response, context="script")

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

    def test_format_code_with_multiline_explanation(self) -> None:
        """Test formatting code with multiline explanation."""
        response = CodeGenerationResponse(
            code="find . -type f -name '*.log' | xargs grep 'ERROR'",
            explanation=(
                "This command does several things:\n1. Finds all .log files\n2. Searches for ERROR in each file"
            ),
            language="bash",
        )

        result = ResponseFormatter.format_code_generation(response)

        assert "```bash" in result
        assert "find . -type f" in result
        assert "1. Finds all .log files" in result
        assert "2. Searches for ERROR" in result

    def test_format_code_with_special_characters(self) -> None:
        """Test formatting code containing special characters."""
        response = CodeGenerationResponse(
            code='#!/usr/bin/env python3\nprint("Test < > & \' \\"")',
            explanation="Script with special chars",
            language="python",
        )

        result = ResponseFormatter.format_code_generation(response)

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
