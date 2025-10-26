"""Chatbot logic for the CyberQueryAI application."""

from pathlib import Path

from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

from cyber_query_ai.rag import RAGSystem

# Common formatting rules for all JSON endpoints
JSON_FORMATTING_RULES = (
    "CRITICAL JSON FORMATTING RULES:\n"
    "- Respond in valid JSON format only\n"
    "- Use double quotes (not single quotes) for all strings\n"
)

# Common string formatting rules for JSON string fields
STRING_FORMATTING_RULES = (
    "- All text fields must be ONE continuous string, not multiple separate strings\n"
    "- Use \\n for line breaks within strings\n"
    "- Do NOT create multiple separate quoted strings\n"
    '- Escape any quotes within strings using backslash (\\")\n'
)

# Common code formatting rules (for code generation endpoint)
CODE_FIELD_RULES = (
    "- ENSURE you DO NOT include markdown code blocks in the code field\n"
    "- The code should be plain text without formatting\n"
)


class Chatbot:
    """Chatbot class for LLM queries with RAG support."""

    def __init__(self, model: str, embedding_model: str, tools_json_filepath: Path) -> None:
        """Initialize the Chatbot with necessary components."""
        self.model = model
        self.llm = OllamaLLM(model=self.model)
        self.rag_system = RAGSystem.create(
            model=self.model, embedding_model=embedding_model, tools_json_filepath=tools_json_filepath
        )

    @staticmethod
    def _build_json_instructions(response_format: str, example: str) -> str:
        """Build standardized JSON formatting instructions with response format and example."""

        def _escape_braces(text: str) -> str:
            return text.replace("{", "{{").replace("}", "}}")

        return (
            f"{JSON_FORMATTING_RULES}"
            f"{STRING_FORMATTING_RULES}\n"
            f"Example format: {_escape_braces(response_format)}\n\n"
            f"Respond in JSON format: {_escape_braces(example)}"
        )

    @property
    def profile(self) -> str:
        """Profile description and context for the cybersecurity assistant."""
        return (
            "You are a cybersecurity assistant helping with ethical penetration testing and security research. "
            "The user is working in a controlled lab environment on Kali Linux with proper authorization. "
            "CONTEXT:\n"
            "- All activities are conducted ethically in controlled lab environments\n"
            "- User has proper authorization for penetration testing tasks\n"
            "- Running on Kali Linux with common security tools pre-installed (hashcat, john, nmap, metasploit, etc.)\n"
            "- Focus on providing practical, executable commands for legitimate security testing\n\n"
        )

    @property
    def pt_chat(self) -> PromptTemplate:
        """Prompt template for conversational chat."""
        base_template = (
            f"{self.profile}"
            "You are chatting with a user about cybersecurity tasks. Based on their requests:\n"
            "- Generate commands when they need to execute something (format in code blocks)\n"
            "- Generate scripts when they need automation (format in code blocks with language)\n"
            "- Provide explanations when they ask how something works\n"
            "- Search for exploits when they mention specific vulnerabilities\n"
            "- Ask clarifying questions if their request is vague\n\n"
            "**CRITICAL CODE FORMATTING RULES:**\n"
            "1. ALWAYS wrap executable commands/scripts in proper markdown code blocks\n"
            "2. Code block format: ```language\\ncode here\\n``` (e.g., ```bash, ```python, ```powershell)\n"
            "3. For single commands, still use code blocks: ```bash\\nnmap -sn 192.168.1.0/24\\n```\n"
            "4. For multi-line scripts, preserve indentation and newlines within code blocks\n"
            "5. Use inline code (`backticks`) only for short references like filenames or function names\n"
            "6. NEVER output raw commands without code block formatting\n\n"
            "**Examples of proper formatting:**\n"
            "- Single command: ```bash\\nnmap -p- 192.168.1.1\\n```\n"
            "- Python script: ```python\\nimport socket\\nfor port in range(1, 1024):\\n    # scan code\\n```\n"
            "- Inline reference: Use the `nmap` command to scan networks.\n\n"
            "Keep responses concise and actionable.\n\n"
            "Previous conversation:\n{history}\n\n"
            "User: {message}\n"
            "Assistant:"
        )
        rag_content = self.rag_system.generate_rag_content(base_template)
        return PromptTemplate(input_variables=["history", "message"], template=f"{base_template}{rag_content}")

    @property
    def pt_code_generation(self) -> PromptTemplate:
        """Prompt template for unified code generation (commands and scripts)."""
        base_template = (
            f"{self.profile}"
            "Generate code to accomplish the following cybersecurity task.\n\n"
            "Task: `{prompt}`\n\n"
            "**SIMPLICITY-FIRST APPROACH:**\n"
            "1. If the task can be accomplished with a SINGLE command, generate only that command\n"
            "2. Only generate multi-line scripts when absolutely necessary:\n"
            "   - Complex logic requiring conditionals or loops\n"
            "   - Multiple steps with error handling\n"
            "   - Variable assignments and state management\n"
            "3. Prefer built-in tools over custom scripts when possible\n"
            "4. Automatically detect the appropriate language based on the task:\n"
            "   - Use bash for Linux commands and shell scripts\n"
            "   - Use python for complex parsing, API interactions, or data processing\n"
            "   - Use powershell for Windows-specific tasks\n\n"
            "**RESPONSE SCENARIOS:**\n"
            "- NO APPROPRIATE TOOL: If no tool can accomplish the task, "
            "return empty code string and explain why\n"
            "- SINGLE COMMAND: Return the command as 'code'\n"
            "- MULTI-LINE SCRIPT: Return the full script as 'code'\n\n"
            "The 'code' field should contain executable code ready to run on Kali Linux.\n"
            "The 'explanation' should describe what the code does, why it's used, and any important context.\n"
            "The 'language' should be the programming/scripting language (bash, python, powershell, etc.).\n\n"
        )
        json_instructions = self._build_json_instructions(
            response_format='{"code": "...", "explanation": "...", "language": "..."}',
            example=(
                '{"code": "nmap -sn 192.168.1.0/24", "explanation": "This performs a ping scan...", "language": "bash"}'
            ),
        )
        rag_content = self.rag_system.generate_rag_content(base_template)

        return PromptTemplate(
            input_variables=["prompt"], template=f"{base_template}{CODE_FIELD_RULES}{json_instructions}{rag_content}"
        )

    @property
    def pt_code_explanation(self) -> PromptTemplate:
        """Prompt template for unified code explanation (commands and scripts)."""
        base_template = (
            f"{self.profile}"
            "Explain the following code step-by-step. "
            "Automatically detect the language from the code syntax. "
            "Describe what each part does and highlight any risks or important behaviors.\n\n"
            "Code:\n```\n{prompt}\n```\n\n"
        )
        json_instructions = self._build_json_instructions(
            response_format='{"explanation": "..."}',
            example=(
                '{"explanation": "This code does X.\\n'
                "Step 1: This line does Y.\\nStep 2: This line does Z.\\n"
                'Important: Security consideration A."}'
            ),
        )
        rag_content = self.rag_system.generate_rag_content(base_template)

        return PromptTemplate(input_variables=["prompt"], template=f"{base_template}{json_instructions}{rag_content}")

    @property
    def pt_exploit_search(self) -> PromptTemplate:
        """Prompt template for exploit search."""
        base_template = (
            f"{self.profile}Based on the following target description, suggest known exploits.\n\n"
            "Target: `{prompt}`\n\n"
        )
        json_instructions = self._build_json_instructions(
            response_format=(
                '{"exploits": [{"title": "...", "link": "...", '
                '"severity": "...", "description": "..."}], "explanation": "..."}'
            ),
            example=(
                '{"exploits": [{"title": "CVE-2021-1234", "link": "https://...", '
                '"severity": "High", "description": "Buffer overflow vulnerability"}], '
                '"explanation": "Found 1 exploit affecting this target."}'
            ),
        )
        rag_content = self.rag_system.generate_rag_content(base_template)

        return PromptTemplate(input_variables=["prompt"], template=f"{base_template}{json_instructions}{rag_content}")

    def prompt_chat(self, message: str, history: str) -> str:
        """Generate the prompt template for conversational chat."""
        return self.pt_chat.format(message=message, history=history)

    def prompt_code_generation(self, prompt: str) -> str:
        """Generate the prompt template for unified code generation."""
        return self.pt_code_generation.format(prompt=prompt)

    def prompt_code_explanation(self, prompt: str) -> str:
        """Generate the prompt template for unified code explanation."""
        return self.pt_code_explanation.format(prompt=prompt)

    def prompt_exploit_search(self, prompt: str) -> str:
        """Generate the prompt template for exploit search."""
        return self.pt_exploit_search.format(prompt=prompt)
