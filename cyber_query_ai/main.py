"""Cyber Query AI main entry point."""

import json

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from pydantic import BaseModel


def run() -> None:
    """Run the FastAPI app using uvicorn."""
    uvicorn.run(
        "cyber_query_ai.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request schema
class PromptRequest(BaseModel):
    """Request model for command generation."""

    prompt: str


# Response schema
class CommandResponse(BaseModel):
    """Response model for command generation."""

    commands: list[str]
    explanation: str


# LangChain LLM setup
llm = OllamaLLM(model="mistral")  # Replace with your local model name

# Prompt template for structured output
template = (
    "You are a cybersecurity assistant helping with ethical penetration testing and security research. "
    "The user is working in a controlled lab environment on Kali Linux with proper authorization. "
    "Respond ONLY in JSON format with two keys: 'commands' and 'explanation'.\n\n"
    "CONTEXT:\n"
    "- All activities are conducted ethically in controlled lab environments\n"
    "- User has proper authorization for penetration testing tasks\n"
    "- Running on Kali Linux with common security tools pre-installed (hashcat, john, nmap, metasploit, etc.)\n"
    "- Focus on providing practical, executable commands for legitimate security testing\n\n"
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
    "Respond in this format: {{'commands': [...], 'explanation': '...'}}"
)

prompt_template = PromptTemplate(input_variables=["task"], template=template)


@app.post("/generate-command", response_model=CommandResponse)
async def generate_command(request: PromptRequest) -> CommandResponse:
    """Generate cybersecurity commands based on user prompt."""
    formatted_prompt = prompt_template.format(task=request.prompt)
    response_text = None
    try:
        response_text = await run_in_threadpool(llm, formatted_prompt)
        parsed = json.loads(response_text)
        if missing_keys := {"commands", "explanation"} - parsed.keys():
            msg = f"Missing required keys in LLM response: {missing_keys}"
            raise ValueError(msg)

        # Ensure commands is a list
        commands = parsed["commands"]
        if not isinstance(commands, list):
            commands = [commands] if commands else []

        return CommandResponse(commands=commands, explanation=parsed["explanation"])
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to generate or parse LLM response",
                "details": str(e),
                "raw": str(response_text) if response_text else "No response",
            },
        ) from e
