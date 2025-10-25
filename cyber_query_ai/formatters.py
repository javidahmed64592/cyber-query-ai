"""Response formatters for converting structured responses to conversational format."""

from cyber_query_ai.models import (
    CommandGenerationResponse,
    ExplanationResponse,
    ExploitSearchResponse,
    ScriptGenerationResponse,
)


class ResponseFormatter:
    """Format specialized endpoint responses for conversational chat."""

    @staticmethod
    def format_command_generation(response: CommandGenerationResponse) -> str:
        """Format command generation response for conversational output."""
        if not response.commands:
            return f"I couldn't generate commands for this task. {response.explanation}"

        commands_str = "\n".join(response.commands)
        return (
            "Here are the commands you can use:\n\n"
            f"```bash\n{commands_str}\n```\n\n"
            f"**Explanation**: {response.explanation}"
        )

    @staticmethod
    def format_script_generation(response: ScriptGenerationResponse, language: str) -> str:
        """Format script generation response for conversational output."""
        return (
            f"I've written a {language} script for you:\n\n"
            f"```{language}\n{response.script}\n```\n\n"
            f"**How it works**: {response.explanation}"
        )

    @staticmethod
    def format_explanation(response: ExplanationResponse, context: str) -> str:
        """Format explanation response for conversational output."""
        if context:
            return f"Let me explain this {context}:\n\n{response.explanation}"
        return f"Let me explain:\n\n{response.explanation}"

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
