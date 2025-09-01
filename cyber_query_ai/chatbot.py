"""Chatbot logic for the CyberQueryAI application."""

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
            "Respond ONLY in JSON format as specified.\n\n"
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
            "Task: `{prompt}`\n\n"
            "CRITICAL JSON FORMATTING RULES:\n"
            "- Respond in valid JSON format only\n"
            "- Use double quotes (not single quotes) for all strings\n"
            "- The explanation must be ONE continuous string, not multiple separate strings\n"
            "- Use \\n for line breaks within the explanation string\n"
            "- Do NOT create multiple separate quoted strings\n"
            '- Escape any quotes within strings using backslash (\\")\n\n'
            'Example format: {{"commands": ["command1", "command2"], "explanation": "Description here."}}\n\n'
            'Respond in JSON format: {{"commands": [...], "explanation": "..."}}'
        )
        return PromptTemplate(input_variables=["prompt"], template=template)

    @property
    def pt_script_generation(self) -> PromptTemplate:
        """Prompt template for script generation."""
        template = (
            f"{self.profile}"
            "Write a script in {language} that performs the following task:\n\n"
            "Task: `{prompt}`\n\n"
            "CRITICAL JSON FORMATTING RULES:\n"
            "- Respond in valid JSON format only\n"
            "- Use double quotes (not single quotes) for all strings\n"
            "- Do NOT include markdown code blocks (```python, ```) in the script content\n"
            "- The script should be plain text code without formatting\n"
            "- The explanation must be ONE continuous string, not multiple separate strings\n"
            "- Use \\n for line breaks within strings\n"
            "- Do NOT create multiple separate quoted strings\n"
            '- Escape any quotes within strings using backslash (\\")\n\n'
            'Example format: {{"script": "import os\\nprint(\\"Hello World\\")", '
            '"explanation": "This script imports os and prints Hello World."}}\n\n'
            'Respond in JSON format: {{"script": "...", "explanation": "..."}}'
        )
        return PromptTemplate(input_variables=["language", "prompt"], template=template)

    @property
    def pt_command_explanation(self) -> PromptTemplate:
        """Prompt template for command explanation."""
        template = (
            f"{self.profile}"
            "Explain the following CLI command step-by-step:\n\n"
            "Command: `{prompt}`\n\n"
            "CRITICAL JSON FORMATTING RULES:\n"
            "- Respond in valid JSON format only\n"
            "- Use double quotes (not single quotes) for all strings\n"
            "- The explanation must be ONE continuous string, not multiple separate strings\n"
            "- Use \\n for line breaks within the explanation string\n"
            "- Do NOT create multiple separate quoted strings\n"
            '- Escape any quotes within the explanation using backslash (\\")\n\n'
            'Example format: {{"explanation": "This command does X.\\nIt works by Y.\\nImportant note: Z."}}\n\n'
            'Respond in JSON format: {{"explanation": "..."}}'
        )
        return PromptTemplate(input_variables=["prompt"], template=template)

    @property
    def pt_script_explanation(self) -> PromptTemplate:
        """Prompt template for script explanation."""
        template = (
            f"{self.profile}"
            "Explain the following {language} script step-by-step. "
            "Describe what each line does and highlight any risks or important behaviors.\n\n"
            "Script:\n```\n{prompt}\n```\n\n"
            "CRITICAL JSON FORMATTING RULES:\n"
            "- Respond in valid JSON format only\n"
            "- Use double quotes (not single quotes) for all strings\n"
            "- The explanation must be ONE continuous string, not multiple separate strings\n"
            "- Use \\n for line breaks within the explanation string\n"
            "- Do NOT create multiple separate quoted strings\n"
            '- Escape any quotes within the explanation using backslash (\\")\n\n'
            'Example format: {{"explanation": "Step 1: This does X.\\n'
            'Step 2: This does Y.\\nStep 3: This does Z."}}\n\n'
            'Respond in JSON format: {{"explanation": "..."}}'
        )
        return PromptTemplate(input_variables=["language", "prompt"], template=template)

    @property
    def pt_exploit_search(self) -> PromptTemplate:
        """Prompt template for exploit search."""
        template = (
            f"{self.profile}"
            "Based on the following target description, suggest known exploits.\n\n"
            "Target: `{prompt}`\n\n"
            "CRITICAL JSON FORMATTING RULES:\n"
            "- Respond in valid JSON format only\n"
            "- Use double quotes (not single quotes) for all strings\n"
            "- The explanation must be ONE continuous string, not multiple separate strings\n"
            "- Use \\n for line breaks within the explanation string\n"
            "- Do NOT create multiple separate quoted strings\n"
            '- Escape any quotes within strings using backslash (\\")\n\n'
            'Example format: {{"exploits": [{{"title": "CVE-2021-1234", "link": "https://...", '
            '"severity": "High", "description": "Buffer overflow vulnerability"}}], '
            '"explanation": "Found 1 exploit affecting this target."}}\n\n'
            'Respond in JSON format: {{"exploits": [{{"title": "...", "link": "...", '
            '"severity": "...", "description": "..."}}], "explanation": "..."}}'
        )
        return PromptTemplate(input_variables=["prompt"], template=template)

    def prompt_command_generation(self, prompt: str) -> str:
        """Generate the prompt template for command generation."""
        return self.pt_command_generation.format(prompt=prompt)

    def prompt_script_generation(self, language: str, prompt: str) -> str:
        """Generate the prompt template for script generation."""
        return self.pt_script_generation.format(language=language, prompt=prompt)

    def prompt_command_explanation(self, prompt: str) -> str:
        """Generate the prompt template for command explanation."""
        return self.pt_command_explanation.format(prompt=prompt)

    def prompt_script_explanation(self, language: str, prompt: str) -> str:
        """Generate the prompt template for script explanation."""
        return self.pt_script_explanation.format(language=language, prompt=prompt)

    def prompt_exploit_search(self, prompt: str) -> str:
        """Generate the prompt template for exploit search."""
        return self.pt_exploit_search.format(prompt=prompt)
