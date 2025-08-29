"""Chatbot logic for the Cyber Query AI application."""

from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM


class Chatbot:
    """Chatbot class for LLM queries."""

    def __init__(self, model: str) -> None:
        """Initialize the Chatbot with necessary components."""
        self.model = model
        self.llm = OllamaLLM(model=self.model)

    @property
    def profile(self) -> str:
        """Profile description and context for the cybersecurity assistant."""
        return (
            "You are a cybersecurity assistant helping with ethical penetration testing and security research. "
            "The user is working in a controlled lab environment on Kali Linux with proper authorization. "
            "Respond ONLY in JSON format with two keys: 'commands' and 'explanation'.\n\n"
            "CONTEXT:\n"
            "- All activities are conducted ethically in controlled lab environments\n"
            "- User has proper authorization for penetration testing tasks\n"
            "- Running on Kali Linux with common security tools pre-installed (hashcat, john, nmap, metasploit, etc.)\n"
            "- Focus on providing practical, executable commands for legitimate security testing\n\n"
        )

    @property
    def pt_command_generation(self) -> PromptTemplate:
        """Prompt template for command generation."""
        template = (
            f"{self.profile}"
            "RESPONSE SCENARIOS:\n"
            "1. NO APPROPRIATE TOOL: If no cybersecurity tool can accomplish the task, "
            "return 'commands': [] (empty array) and explain why in 'explanation'.\n"
            "2. SINGLE COMMAND: If one command accomplishes the task, "
            "return 'commands': ['command'] (array with one string).\n"
            "3. MULTIPLE ALTERNATIVES: If multiple tools/commands could work, "
            "return 'commands': ['cmd1', 'cmd2', ...] and compare them in 'explanation'.\n"
            "4. SEQUENTIAL WORKFLOW: If multiple commands must be run in order, "
            "return 'commands': ['step1', 'step2', ...] and explain the workflow in 'explanation'.\n\n"
            "The 'commands' array should contain exact CLI commands ready to execute on Kali Linux. "
            "The 'explanation' should describe what the commands do, why they're used, and any important context.\n\n"
            "Task: {task}\n\n"
            "Respond in JSON format: {{'commands': [...], 'explanation': '...'}}"
        )
        return PromptTemplate(input_variables=["task"], template=template)

    def prompt_command_generation(self, task: str) -> str:
        """Generate the prompt template for command generation."""
        return self.pt_command_generation.format(task=task)
