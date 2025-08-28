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
    prompt: str


# Response schema
class CommandResponse(BaseModel):
    command: str
    explanation: str


# LangChain LLM setup
llm = OllamaLLM(model="mistral")  # Replace with your local model name

# Prompt template for structured output
template = (
    "You are a cybersecurity assistant. Respond ONLY in JSON format with two keys: 'command' and 'explanation'. "
    "The 'command' should contain the exact CLI command to perform the task. "
    "The 'explanation' should describe what the command does and why it's used.\n"
    "Task: {task}\n"
    "Respond in this format: {{'command': '...', 'explanation': '...'}}"
)

prompt_template = PromptTemplate(input_variables=["task"], template=template)


@app.post("/generate-command", response_model=CommandResponse)
async def generate_command(request: PromptRequest):
    formatted_prompt = prompt_template.format(task=request.prompt)
    response_text = None
    try:
        response_text = await run_in_threadpool(llm, formatted_prompt)
        parsed = json.loads(response_text)
        if not ("command" in parsed and "explanation" in parsed):
            msg = "Missing required keys in LLM response"
            raise ValueError(msg)
        return CommandResponse(command=parsed["command"], explanation=parsed["explanation"])
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to generate or parse LLM response",
                "details": str(e),
                "raw": str(response_text) if response_text else "No response",
            },
        ) from e
