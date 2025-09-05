"""RAG system for the CyberQueryAI application."""

from __future__ import annotations

import json

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


class ToolsMetadata(BaseModel):
    """Metadata for a cybersecurity tool."""

    name: str
    file: str
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

    def __init__(self, model: str, embedding_model: str = "nomic-embed-text") -> None:
        """Initialize the RAG system."""
        self.model = model
        self.embedding_model = embedding_model
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

        if not RAG_DATA_DIR.exists():
            return documents

        tool_suite = ToolSuite.from_json(str(TOOLS_FILEPATH))

        # Load all .txt files from rag_data directory
        for txt_file in RAG_DATA_DIR.glob("*.txt"):
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

    def split_documents(self, documents: list[Document]) -> list[Document]:
        """Split documents into smaller chunks for better retrieval."""
        if not documents:
            return []

        return self.text_splitter.split_documents(documents)

    def create_vector_store(self) -> InMemoryVectorStore:
        """Create or return existing vector store."""
        if self.vector_store is not None:
            return self.vector_store

        # Load and split documents
        documents = self.load_documents()
        if not documents:
            self.vector_store = InMemoryVectorStore(self.embeddings)
            return self.vector_store

        splits = self.split_documents(documents)

        # Create vector store and add documents
        self.vector_store = InMemoryVectorStore(self.embeddings)

        if splits:
            self.vector_store.add_documents(splits)

        return self.vector_store

    def get_relevant_context(self, query: str, k: int = 4) -> list[Document]:
        """Retrieve relevant documents for a given query."""
        try:
            return self.vector_store.similarity_search(query, k=k)
        except Exception:
            return []

    def format_context(self, documents: list[Document]) -> str:
        """Format retrieved documents into a context string with rich metadata."""
        if not documents:
            return ""

        context_parts = []
        for doc in documents:
            tool = doc.metadata.get("tool", "unknown")
            source = doc.metadata.get("source", "unknown")
            category = doc.metadata.get("category", "")
            description = doc.metadata.get("description", "")
            tags = doc.metadata.get("tags", [])
            content = doc.page_content.strip()

            # Build header with metadata
            header_parts = [f"Tool: {tool}"]
            if category:
                header_parts.append(f"Category: {category}")
            if description:
                header_parts.append(f"Description: {description}")
            if tags:
                header_parts.append(f"Tags: {', '.join(tags)}")

            header = " | ".join(header_parts)
            context_parts.append(f"[{header}]\nSource: {source}\n\n{content}")

        return "\n\n" + "=" * 80 + "\n\n".join(context_parts)

    def is_available(self) -> bool:
        """Check if the RAG system is available and ready to use."""
        try:
            if self.vector_store is None:
                self.create_vector_store()
        except Exception:
            return False
        else:
            return self.vector_store is not None

    def get_context_for_template(self, query: str) -> str:
        """Get RAG context for a specific query."""
        if not self.is_available():
            return ""

        if relevant_docs := self.vector_store.similarity_search(query):
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


def create_rag_system(model: str = "llama3.2") -> RAGSystem:
    """Create and initialize the RAG system."""
    rag_system = RAGSystem(model=model)
    rag_system.create_vector_store()
    return rag_system
