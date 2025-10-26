"""Response formatters for converting structured responses to conversational format."""

from cyber_query_ai.models import (
    CodeExplanationResponse,
    CodeGenerationResponse,
    ExploitSearchResponse,
)


class ResponseFormatter:
    """Format specialized endpoint responses for conversational chat."""

    @staticmethod
    def format_code_generation(response: CodeGenerationResponse) -> str:
        """Format code generation response for conversational output.

        Automatically detects single-line commands vs multi-line scripts.
        """
        if not response.code:
            return f"I couldn't generate code for this task. {response.explanation}"

        # Auto-detect multiline based on presence of newlines
        is_multiline = "\n" in response.code
        if is_multiline:
            header = f"I've written a {response.language} script for you:"
        else:
            header = "Here's the command you can use:"

        return f"{header}\n\n```{response.language}\n{response.code}\n```\n\n**Explanation**: {response.explanation}"

    @staticmethod
    def format_explanation(response: CodeExplanationResponse, context: str = "code") -> str:
        """Format explanation response for conversational output."""
        return f"Let me explain this {context}:\n\n{response.explanation}"

    @staticmethod
    def format_exploit_search(response: ExploitSearchResponse) -> str:
        """Format exploit search response for conversational output."""
        if not response.exploits:
            return f"No exploits found. {response.explanation}"

        exploits_str = [
            f"### {exploit.title} ({exploit.severity})\n"
            f"**Description**: {exploit.description}\n"
            f"**Link**: {exploit.link}\n"
            for exploit in response.exploits
        ]

        exploit_count = len(response.exploits)
        plural = "vulnerability" if exploit_count == 1 else "vulnerabilities"

        return (
            f"I found {exploit_count} {plural}:\n\n"
            + "\n".join(exploits_str)
            + f"\n**Summary**: {response.explanation}"
        )
