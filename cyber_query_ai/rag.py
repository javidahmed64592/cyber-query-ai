"""RAG system for the CyberQueryAI application."""

from __future__ import annotations

import json
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import BaseModel

from cyber_query_ai.config import get_root_dir

RAG_DATA_DIR = get_root_dir() / "rag_data"
TOOLS_FILENAME = "tools.json"
TOOLS_FILEPATH = RAG_DATA_DIR / TOOLS_FILENAME
EMBEDDING_MODEL = "bge-m3"


class ToolsMetadata(BaseModel):
    """Metadata for a cybersecurity tool."""

    file: str
    name: str
    type: str
    category: str
    subcategory: str
    description: str
    tags: list[str]
    use_cases: list[str]

    @property
    def metadata_dict(self) -> dict:
        """Return metadata as a dictionary."""
        return {
            "source": self.file,
            "tool": self.name,
            "type": self.type,
            "category": self.category,
            "subcategory": self.subcategory,
            "description": self.description,
            "tags": self.tags,
            "use_cases": self.use_cases,
        }


class ToolSuite(BaseModel):
    """Suite of cybersecurity tools."""

    tools: dict[str, ToolsMetadata]

    @classmethod
    def from_json(cls, filepath: str) -> ToolSuite:
        """Load tools metadata from a JSON file."""
        try:
            with open(filepath, encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return cls(tools={})

        tools = {name: ToolsMetadata(**info) for name, info in data.items()}
        return cls(tools=tools)


class RAGSystem:
    """RAG (Retrieval-Augmented Generation) system for cybersecurity documentation."""

    def __init__(self, model: str, embedding_model: str, tools_json_filepath: Path) -> None:
        """Initialize the RAG system."""
        self.model = model
        self.embedding_model = embedding_model
        self.tools_json_filepath = tools_json_filepath

        self.embeddings = OllamaEmbeddings(model=embedding_model)
        self.vector_store: InMemoryVectorStore | None = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True,
        )

    def load_documents(self) -> list[Document]:
        """Load all text documents from the rag_data directory with JSON metadata."""
        documents = []

        if not self.tools_json_filepath.exists():
            return documents

        tool_suite = ToolSuite.from_json(str(self.tools_json_filepath))

        # Load all .txt files from rag_data directory
        for txt_file in self.tools_json_filepath.parent.glob("*.txt"):
            loader = TextLoader(str(txt_file), encoding="utf-8")
            docs = loader.load()

            # Find metadata for this file
            for tool in tool_suite.tools.values():
                if tool.file == txt_file.name:
                    # Add metadata to each document
                    for doc in docs:
                        doc.metadata.update(tool.metadata_dict)

            documents.extend(docs)

        return documents

    def create_vector_store(self) -> None:
        """Create or return existing vector store."""
        if self.vector_store is not None:
            return

        # Create vector store
        self.vector_store = InMemoryVectorStore(self.embeddings)

        # Load and split documents
        if documents := self.load_documents():
            if splits := self.text_splitter.split_documents(documents):
                self.vector_store.add_documents(splits)

    def format_context(self, documents: list[Document]) -> str:
        """Format retrieved documents into a context string with rich metadata."""
        if not documents:
            return ""

        context_parts = []
        for doc in documents:
            tool = doc.metadata.get("tool", "unknown")
            source = doc.metadata.get("source", "unknown")
            content = doc.page_content.strip()

            # Build header with metadata
            header_parts = [f"Tool: {tool}"]
            if category := doc.metadata.get("category", ""):
                header_parts.append(f"Category: {category}")
            if subcategory := doc.metadata.get("subcategory", ""):
                header_parts.append(f"Subcategory: {subcategory}")
            if description := doc.metadata.get("description", ""):
                header_parts.append(f"Description: {description}")
            if tags := doc.metadata.get("tags", []):
                header_parts.append(f"Tags: {', '.join(tags)}")
            if use_cases := doc.metadata.get("use_cases", []):
                header_parts.append(f"Use Cases: {', '.join(use_cases)}")

            header = " | ".join(header_parts)
            context_parts.append(f"[{header}]\nSource: {source}\n\n{content}")

        return "\n\n" + "=" * 80 + "\n\n".join(context_parts)

    def get_context_for_template(self, query: str) -> str:
        """Get RAG context for a specific query."""
        if not self.vector_store:
            return ""

        if relevant_docs := self.vector_store.similarity_search(query, k=3):
            return self.format_context(relevant_docs)

        return ""

    def generate_rag_content(self, query: str) -> str:
        """Generate RAG context."""
        if rag_context := self.get_context_for_template(query):
            return (
                f"\nRELEVANT DOCUMENTATION:\n"
                f"{rag_context.replace('{', '{{').replace('}', '}}')}\n\n"
                f"Use the above documentation to provide more accurate and detailed responses. "
                f"Reference specific tool options, syntax, and examples from the documentation when relevant.\n\n"
            )

        return ""


def create_rag_system(model: str) -> RAGSystem:
    """Create and initialize the RAG system."""
    rag_system = RAGSystem(model=model, embedding_model=EMBEDDING_MODEL, tools_json_filepath=TOOLS_FILEPATH)
    rag_system.create_vector_store()
    return rag_system
